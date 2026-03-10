from __future__ import annotations

import json
import threading
from typing import Any, TypedDict
from uuid import uuid4

from langgraph.graph import END, START, StateGraph
from langgraph.types import Command, interrupt

from backend.app.persistent_checkpointer import PersistentInMemorySaver
from backend.agents.explainer_agent import generate_explanation
from backend.agents.parser_agent import parse_question
from backend.agents.router_agent import route_problem
from backend.agents.solvers.solver_dispatcher import run_solver
from backend.agents.verifier_agent import verify_solution
from backend.memory.memory_store import (
    get_workflow_runtime,
    save_feedback,
    save_interaction,
    save_learning_signal,
    save_retrieval,
    save_verifier_outcome,
    upsert_workflow_runtime,
)
from backend.models.schemas import AgentTraceStep, LearningSignalDraft, SolveRequest
from backend.rag.retriever import append_example_to_vector_store


class WorkflowGraphState(TypedDict, total=False):
    input_type: str | None
    original_input: str | None
    working_input: str | None
    ocr_confidence: float | None
    asr_confidence: float | None
    input_reviewed: bool
    recheck_requested: bool
    solver_feedback: str | None
    status: str
    message: str | None
    next_step: str
    review_stage: str | None
    final_action: str | None
    learning_signals: list[dict[str, Any]]
    trace: list[dict[str, Any]]
    parsed_problem: dict[str, Any] | None
    route: dict[str, Any] | None
    solver_output: dict[str, Any] | None
    verification: dict[str, Any] | None
    explanation: str | None
    interaction_id: int | None


class WorkflowController:
    INPUT_CONFIDENCE_THRESHOLD = 0.75
    VERIFIER_CONFIDENCE_THRESHOLD = 0.70
    NODE_AGENTS = {
        "input_gate": "Input Gate",
        "parse": "Parser Agent",
        "parser_gate": "Parser Gate",
        "route": "Intent Router Agent",
        "solve": "Solver Agent",
        "verify": "Verifier Agent",
        "solver_gate": "Solver Gate",
        "explain": "Explainer Agent",
        "final_gate": "Final Review",
        "persist": "Memory Layer",
    }

    def __init__(self):
        graph = StateGraph(WorkflowGraphState)
        graph.add_node("input_gate", self._input_gate)
        graph.add_node("parse", self._parse_problem)
        graph.add_node("parser_gate", self._parser_gate)
        graph.add_node("route", self._route_problem)
        graph.add_node("solve", self._solve_problem)
        graph.add_node("verify", self._verify_solution)
        graph.add_node("solver_gate", self._solver_gate)
        graph.add_node("explain", self._explain_solution)
        graph.add_node("final_gate", self._final_gate)
        graph.add_node("persist", self._persist_result)

        graph.add_edge(START, "input_gate")
        graph.add_conditional_edges(
            "input_gate",
            self._next_step,
            {"parse": "parse", "input_gate": "input_gate", "end": END},
        )
        graph.add_edge("parse", "parser_gate")
        graph.add_conditional_edges(
            "parser_gate",
            self._next_step,
            {"route": "route", "parse": "parse", "parser_gate": "parser_gate", "end": END},
        )
        graph.add_edge("route", "solve")
        graph.add_edge("solve", "verify")
        graph.add_edge("verify", "solver_gate")
        graph.add_conditional_edges(
            "solver_gate",
            self._next_step,
            {"explain": "explain", "solver_gate": "solver_gate", "end": END},
        )
        graph.add_edge("explain", "final_gate")
        graph.add_conditional_edges(
            "final_gate",
            self._next_step,
            {"persist": "persist", "solve": "solve", "final_gate": "final_gate", "end": END},
        )
        graph.add_edge("persist", END)

        self.checkpointer = PersistentInMemorySaver()
        self.graph = graph.compile(checkpointer=self.checkpointer)
        self._active_runs: dict[str, threading.Thread] = {}
        self._active_lock = threading.Lock()

    def run(self, request: SolveRequest):
        thread_id = request.thread_id or str(uuid4())
        config, graph_input, error_response = self._prepare_graph_execution(request, thread_id)
        if error_response is not None:
            self._save_runtime_response(thread_id, error_response)
            return error_response

        try:
            running_response = self._build_running_response(
                thread_id,
                current_node=None,
                current_agent=None,
                state_values=None,
                message="Workflow started.",
            )
            self._save_runtime_response(thread_id, running_response)

            result = self.graph.invoke(graph_input, config=config)
            snapshot = self.graph.get_state(config)
            response = self._build_response_from_result(
                thread_id,
                result=result,
                state_values=snapshot.values or {},
                interrupts=snapshot.interrupts,
            )
            self._save_runtime_response(thread_id, response)
            return response
        except Exception as exc:  # noqa: BLE001
            state_values = self._safe_state_values(config)
            error = self._build_error_response(thread_id, exc, state_values)
            self._save_runtime_response(thread_id, error)
            return error

    def run_async(self, request: SolveRequest):
        thread_id = request.thread_id or str(uuid4())
        config, _, error_response = self._prepare_graph_execution(request, thread_id)
        if error_response is not None:
            self._save_runtime_response(thread_id, error_response)
            return error_response

        with self._active_lock:
            worker = self._active_runs.get(thread_id)
            if worker is not None and worker.is_alive():
                return self.get_status(thread_id)

            accepted = {
                "status": "accepted",
                "thread_id": thread_id,
                "message": "Workflow started.",
                "trace": self._safe_state_values(config).get("trace", []),
                "retrieved_context": self._safe_retrieved_context(config),
                "current_node": None,
                "current_agent": None,
            }
            self._save_runtime_response(thread_id, accepted)

            worker = threading.Thread(
                target=self._execute_async,
                args=(request, thread_id),
                daemon=True,
            )
            self._active_runs[thread_id] = worker
            worker.start()

        return accepted

    def get_status(self, thread_id: str):
        runtime = get_workflow_runtime(thread_id)
        if runtime is None:
            return {
                "status": "error",
                "thread_id": thread_id,
                "message": "thread_id was not found.",
                "trace": [],
                "retrieved_context": [],
                "current_node": None,
                "current_agent": None,
            }

        response = dict(runtime.get("response") or {})
        response.setdefault("status", runtime["status"])
        response["thread_id"] = thread_id
        response["trace"] = runtime.get("trace", []) or response.get("trace", [])
        response["retrieved_context"] = (
            runtime.get("retrieved_context", [])
            or response.get("retrieved_context", [])
        )
        response["current_node"] = runtime.get("current_node")
        response["current_agent"] = runtime.get("current_agent")

        if runtime.get("error"):
            response["message"] = runtime["error"]
        elif runtime.get("message"):
            response.setdefault("message", runtime["message"])

        return response

    def _execute_async(self, request: SolveRequest, thread_id: str):
        try:
            self._run_async_workflow(request, thread_id)
        finally:
            with self._active_lock:
                worker = self._active_runs.get(thread_id)
                if worker is threading.current_thread():
                    del self._active_runs[thread_id]

    def _run_async_workflow(self, request: SolveRequest, thread_id: str):
        config, graph_input, error_response = self._prepare_graph_execution(request, thread_id)
        if error_response is not None:
            self._save_runtime_response(thread_id, error_response)
            return

        interrupt_payload = None

        try:
            self._save_runtime_response(
                thread_id,
                self._build_running_response(
                    thread_id,
                    current_node=None,
                    current_agent=None,
                    state_values=self._safe_state_values(config),
                    message="Workflow started.",
                ),
            )

            for stream_mode, payload in self.graph.stream(
                graph_input,
                config=config,
                stream_mode=["tasks", "updates"],
            ):
                if stream_mode == "tasks":
                    task_name = payload.get("name")
                    if "input" in payload:
                        self._save_runtime_response(
                            thread_id,
                            self._build_running_response(
                                thread_id,
                                current_node=task_name,
                                current_agent=self.NODE_AGENTS.get(task_name, task_name),
                                state_values=self._safe_state_values(config),
                                message=f"{self.NODE_AGENTS.get(task_name, task_name)} is running.",
                            ),
                        )
                    else:
                        self._save_runtime_response(
                            thread_id,
                            self._build_running_response(
                                thread_id,
                                current_node=None,
                                current_agent=None,
                                state_values=self._safe_state_values(config),
                                message=None,
                            ),
                        )
                elif stream_mode == "updates":
                    if "__interrupt__" in payload:
                        interrupt_payload = payload["__interrupt__"][0].value

                    self._save_runtime_response(
                        thread_id,
                        self._build_running_response(
                            thread_id,
                            current_node=None,
                            current_agent=None,
                            state_values=self._safe_state_values(config),
                            message="Workflow is progressing.",
                        ),
                    )

            snapshot = self.graph.get_state(config)
            response = self._build_response_from_result(
                thread_id,
                result=snapshot.values or {},
                state_values=snapshot.values or {},
                interrupts=snapshot.interrupts,
                interrupt_payload=interrupt_payload,
            )
            self._save_runtime_response(thread_id, response)
        except Exception as exc:  # noqa: BLE001
            error = self._build_error_response(thread_id, exc, self._safe_state_values(config))
            self._save_runtime_response(thread_id, error)

    def _prepare_graph_execution(self, request: SolveRequest, thread_id: str):
        config = {"configurable": {"thread_id": thread_id}}

        if request.review is not None:
            if request.thread_id is None:
                return config, None, {
                    "status": "error",
                    "thread_id": thread_id,
                    "message": "thread_id is required to resume a LangGraph workflow.",
                    "trace": [],
                    "retrieved_context": [],
                }
            if not self.checkpointer.has_thread(thread_id):
                return config, None, {
                    "status": "error",
                    "thread_id": thread_id,
                    "message": "thread_id was not found. Start a new question or retry before the session expires.",
                    "trace": [],
                    "retrieved_context": [],
                }
            return config, Command(resume=request.review.model_dump()), None

        if request.input_type is None:
            return config, None, {
                "status": "error",
                "thread_id": thread_id,
                "message": "input_type is required for a new workflow run.",
                "trace": [],
                "retrieved_context": [],
            }

        return config, {
            "input_type": request.input_type,
            "original_input": request.text,
            "working_input": request.text,
            "ocr_confidence": request.ocr_confidence,
            "asr_confidence": request.asr_confidence,
            "input_reviewed": request.input_reviewed,
            "recheck_requested": request.recheck_requested,
            "solver_feedback": None,
            "status": "running",
            "message": None,
            "review_stage": None,
            "final_action": None,
            "learning_signals": [],
            "trace": [],
        }, None

    def _build_response_from_result(
        self,
        thread_id: str,
        *,
        result: dict[str, Any],
        state_values: dict[str, Any],
        interrupts,
        interrupt_payload=None,
    ):
        if "__interrupt__" in result:
            interrupt_payload = result["__interrupt__"][0].value

        if interrupt_payload is None and interrupts:
            interrupt_payload = interrupts[0].value

        if interrupt_payload is not None:
            return self._build_interrupt_response(thread_id, interrupt_payload, state_values)

        if result.get("status") == "rejected":
            return self._build_rejected_response(thread_id, result)

        return self._build_success_response(thread_id, result)

    def _build_interrupt_response(self, thread_id: str, payload, state_values: dict[str, Any]):
        return {
            "status": "hitl_required",
            "thread_id": thread_id,
            "trace": state_values.get("trace", []),
            "retrieved_context": (state_values.get("solver_output", {}) or {}).get(
                "retrieved_context", []
            ),
            "current_node": None,
            "current_agent": None,
            **payload,
        }

    def _build_rejected_response(self, thread_id: str, result: dict[str, Any]):
        return {
            "status": "rejected",
            "thread_id": thread_id,
            "stage": result.get("review_stage"),
            "message": result.get("message", "The workflow was rejected by human review."),
            "trace": result.get("trace", []),
            "retrieved_context": (result.get("solver_output", {}) or {}).get(
                "retrieved_context", []
            ),
            "current_node": None,
            "current_agent": None,
        }

    def _build_success_response(self, thread_id: str, result: dict[str, Any]):
        return {
            "status": "success",
            "thread_id": thread_id,
            "interaction_id": result.get("interaction_id"),
            "final_action": result.get("final_action"),
            "problem": result["parsed_problem"]["problem_text"],
            "solution": result["solver_output"]["solution"],
            "retrieved_context": result["solver_output"].get("retrieved_context", []),
            "verification": result["verification"],
            "confidence": result["verification"]["confidence"],
            "explanation": result.get("explanation"),
            "trace": result.get("trace", []),
            "learning_signals_saved": len(result.get("learning_signals", [])),
            "current_node": None,
            "current_agent": None,
        }

    def _build_running_response(
        self,
        thread_id: str,
        *,
        current_node: str | None,
        current_agent: str | None,
        state_values: dict[str, Any] | None,
        message: str | None,
    ):
        state_values = state_values or {}
        return {
            "status": "running",
            "thread_id": thread_id,
            "message": message or "Workflow is running.",
            "trace": state_values.get("trace", []),
            "retrieved_context": (state_values.get("solver_output", {}) or {}).get(
                "retrieved_context", []
            ),
            "current_node": current_node,
            "current_agent": current_agent,
        }

    def _build_error_response(
        self,
        thread_id: str,
        exc: Exception,
        state_values: dict[str, Any] | None,
    ):
        state_values = state_values or {}
        return {
            "status": "error",
            "thread_id": thread_id,
            "message": f"{type(exc).__name__}: {exc}",
            "trace": state_values.get("trace", []),
            "retrieved_context": (state_values.get("solver_output", {}) or {}).get(
                "retrieved_context", []
            ),
            "current_node": None,
            "current_agent": None,
        }

    def _save_runtime_response(self, thread_id: str, response: dict[str, Any]):
        upsert_workflow_runtime(
            thread_id,
            status=response.get("status"),
            current_node=response.get("current_node"),
            current_agent=response.get("current_agent"),
            message=response.get("message"),
            trace=response.get("trace"),
            retrieved_context=response.get("retrieved_context"),
            response=response,
            error=response.get("message") if response.get("status") == "error" else None,
        )

    def _safe_state_values(self, config):
        try:
            snapshot = self.graph.get_state(config)
        except Exception:  # noqa: BLE001
            return {}

        return snapshot.values or {}

    def _safe_retrieved_context(self, config):
        state_values = self._safe_state_values(config)
        return (state_values.get("solver_output", {}) or {}).get("retrieved_context", [])

    def _input_gate(self, state: WorkflowGraphState):
        if not self._needs_input_review(state):
            return {
                "next_step": "parse",
                "message": None,
                "trace": self._append_trace(
                    state,
                    "Input Gate",
                    "pass",
                    "Input confidence is acceptable or not provided.",
                    output={"next_step": "parse"},
                ),
            }

        review = interrupt(
            {
                "stage": "input_review",
                "message": state.get("message")
                or "OCR/ASR confidence is low. Approve the transcript or edit it before parsing.",
                "details": {
                    "input_text": state.get("working_input"),
                    "ocr_confidence": state.get("ocr_confidence"),
                    "asr_confidence": state.get("asr_confidence"),
                },
            }
        )
        return self._handle_input_review(state, review)

    def _parse_problem(self, state: WorkflowGraphState):
        parsed_problem = parse_question(state.get("working_input") or "")
        return {
            "parsed_problem": parsed_problem.model_dump(),
            "message": None,
            "trace": self._append_trace(
                state,
                "Parser Agent",
                "parse",
                "Converted input into a structured math problem.",
                output=parsed_problem.model_dump(),
            ),
        }

    def _parser_gate(self, state: WorkflowGraphState):
        parsed_problem = state["parsed_problem"]

        if not parsed_problem.get("needs_clarification"):
            return {
                "next_step": "route",
                "message": None,
                "trace": self._append_trace(
                    state,
                    "Parser Gate",
                    "pass",
                    "No clarification is required.",
                    output={"next_step": "route"},
                ),
            }

        review = interrupt(
            {
                "stage": "parser_review",
                "message": state.get("message")
                or "The parser marked this problem as ambiguous. Approve it or edit the problem statement and re-run parsing.",
                "details": {
                    "input_text": state.get("working_input"),
                    "parsed_problem": parsed_problem,
                },
            }
        )
        return self._handle_parser_review(state, review)

    def _route_problem(self, state: WorkflowGraphState):
        route = route_problem(state["parsed_problem"])
        return {
            "route": route.model_dump(),
            "trace": self._append_trace(
                state,
                "Intent Router Agent",
                "route",
                f"Selected {route.solver} from detected topics.",
                output=route.model_dump(),
            ),
        }

    def _solve_problem(self, state: WorkflowGraphState):
        solver = run_solver(state["route"]["solver"])
        solver_output = solver.solve(
            state["parsed_problem"],
            reviewer_feedback=state.get("solver_feedback"),
        )
        return {
            "solver_output": solver_output.model_dump(),
            "solver_feedback": None,
            "message": None,
            "trace": self._append_trace(
                state,
                "Solver Agent",
                "solve",
                f"Generated a candidate solution using {len(solver_output.retrieved_context)} retrieved context items.",
                output={
                    "solution": solver_output.solution,
                },
            ),
        }

    def _verify_solution(self, state: WorkflowGraphState):
        verification = verify_solution(
            state["parsed_problem"]["problem_text"],
            state["solver_output"]["solution"],
        )
        return {
            "verification": verification.model_dump(),
            "message": None,
            "trace": self._append_trace(
                state,
                "Verifier Agent",
                "verify",
                f"Checked correctness with confidence {verification.confidence:.2f}.",
                output=verification.model_dump(),
            ),
        }

    def _solver_gate(self, state: WorkflowGraphState):
        verification = state["verification"]
        needs_review = state.get("recheck_requested") or (
            not verification["is_correct"]
            or verification["confidence"] < self.VERIFIER_CONFIDENCE_THRESHOLD
        )

        if not needs_review:
            return {
                "next_step": "explain",
                "message": None,
                "recheck_requested": False,
                "trace": self._append_trace(
                    state,
                    "Solver Gate",
                    "pass",
                    "Verifier marked the solution correct with acceptable confidence.",
                    output={"next_step": "explain"},
                ),
            }

        review = interrupt(
            {
                "stage": "solver_review",
                "message": state.get("message")
                or "The verifier is not confident, marked the answer incorrect, or a re-check was requested. Approve, edit, or re-check the solver with feedback.",
                "details": {
                    "problem": state["parsed_problem"]["problem_text"],
                    "candidate_solution": state["solver_output"]["solution"],
                    "verification": verification,
                },
            }
        )
        return self._handle_solver_review(state, review)

    def _explain_solution(self, state: WorkflowGraphState):
        explanation = generate_explanation(
            state["parsed_problem"]["problem_text"],
            state["solver_output"]["solution"],
        )
        return {
            "explanation": explanation.explanation,
            "trace": self._append_trace(
                state,
                "Explainer Agent",
                "explain",
                "Prepared a student-friendly explanation.",
                output=explanation.explanation,
            ),
        }

    def _final_gate(self, state: WorkflowGraphState):
        review = interrupt(
            {
                "stage": "final_review",
                "message": state.get("message")
                or "Review the final solution. You can approve it, edit it, or reject it.",
                "details": {
                    "problem": state["parsed_problem"]["problem_text"],
                    "solution": state["solver_output"]["solution"],
                    "verification": state["verification"],
                    "explanation": state.get("explanation"),
                },
            }
        )
        return self._handle_final_review(state, review)

    def _persist_result(self, state: WorkflowGraphState):
        interaction_id = save_interaction(
            input_type=state.get("input_type"),
            raw_input=state.get("original_input"),
            parsed_problem=state["parsed_problem"],
            topic=state["parsed_problem"]["topics"],
            solution=state["solver_output"]["solution"],
            explanation=state.get("explanation"),
            confidence=state["verification"]["confidence"],
        )

        save_retrieval(interaction_id, state["solver_output"].get("retrieved_context", []))
        save_verifier_outcome(
            interaction_id,
            is_correct=state["verification"]["is_correct"],
            confidence=state["verification"]["confidence"],
            issues=state["verification"].get("issues", []),
        )

        save_feedback(
            interaction_id,
            feedback_type=f"final_review_{state.get('final_action', 'approve')}",
            comment=None,
        )

        for signal in state.get("learning_signals", []):
            save_learning_signal(
                interaction_id=interaction_id,
                stage=signal["stage"],
                signal_type=signal["signal_type"],
                original_value=signal.get("original_value"),
                corrected_value=signal.get("corrected_value"),
                notes=signal.get("notes"),
            )

        append_example_to_vector_store(
            problem=state["parsed_problem"]["problem_text"],
            solution=state["solver_output"]["solution"],
            topics=state["parsed_problem"]["topics"],
            source="human_approved",
        )

        return {
            "interaction_id": interaction_id,
            "status": "success",
            "review_stage": "final_review",
            "trace": self._append_trace(
                state,
                "Memory Layer",
                "persist",
                "Stored interaction, retrieval context, verifier outcome, and learning signals.",
                output={"interaction_id": interaction_id},
            ),
        }

    def _handle_input_review(self, state: WorkflowGraphState, review: dict[str, Any]):
        if review.get("stage") != "input_review":
            return {
                "next_step": "input_gate",
                "message": "Expected review for input_review.",
            }

        action = review.get("action")

        if action == "reject":
            return self._reject(state, "input_review")

        if action == "approve":
            return {
                "input_reviewed": True,
                "next_step": "parse",
                "message": None,
                "trace": self._append_trace(
                    state,
                    "Input Gate",
                    "approve",
                    "Human approved the extracted text.",
                    output={"next_step": "parse"},
                ),
            }

        if action != "edit":
            return {
                "next_step": "input_gate",
                "message": "Input review supports approve, edit, or reject.",
            }

        if not review.get("feedback"):
            return {
                "next_step": "input_gate",
                "message": "Provide corrected transcript text to continue.",
            }

        return {
            "working_input": review["feedback"],
            "input_reviewed": True,
            "learning_signals": self._append_learning_signal(
                state,
                LearningSignalDraft(
                    stage="input_review",
                    signal_type="transcript_correction",
                    original_value=state.get("working_input"),
                    corrected_value=review["feedback"],
                ),
            ),
            "parsed_problem": None,
            "route": None,
            "solver_output": None,
            "verification": None,
            "explanation": None,
            "next_step": "parse",
            "message": None,
            "trace": self._append_trace(
                state,
                "Input Gate",
                "edit",
                "Human edited the extracted text before parsing.",
                output={"working_input": review["feedback"]},
            ),
        }

    def _handle_parser_review(self, state: WorkflowGraphState, review: dict[str, Any]):
        if review.get("stage") != "parser_review":
            return {
                "next_step": "parser_gate",
                "message": "Expected review for parser_review.",
            }

        action = review.get("action")

        if action == "reject":
            return self._reject(state, "parser_review")

        if action == "approve":
            return {
                "next_step": "route",
                "message": None,
                "trace": self._append_trace(
                    state,
                    "Parser Gate",
                    "approve",
                    "Human accepted the ambiguous parse.",
                    output={"next_step": "route"},
                ),
            }

        if action != "edit":
            return {
                "next_step": "parser_gate",
                "message": "Parser review supports approve, edit, or reject.",
            }

        if not review.get("feedback"):
            return {
                "next_step": "parser_gate",
                "message": "Provide an edited problem statement to re-run the parser.",
            }

        return {
            "working_input": review["feedback"],
            "learning_signals": self._append_learning_signal(
                state,
                LearningSignalDraft(
                    stage="parser_review",
                    signal_type="parser_clarification",
                    original_value=state.get("working_input"),
                    corrected_value=review["feedback"],
                ),
            ),
            "parsed_problem": None,
            "route": None,
            "solver_output": None,
            "verification": None,
            "explanation": None,
            "next_step": "parse",
            "message": None,
            "trace": self._append_trace(
                state,
                "Parser Gate",
                "edit",
                "Human clarified the problem statement and requested a fresh parse.",
                output={"working_input": review["feedback"]},
            ),
        }

    def _handle_solver_review(self, state: WorkflowGraphState, review: dict[str, Any]):
        if review.get("stage") != "solver_review":
            return {
                "next_step": "solver_gate",
                "message": "Expected review for solver_review.",
            }

        if review.get("action") == "reject":
            return self._reject(state, "solver_review")

        if review.get("action") == "approve":
            return {
                "next_step": "explain",
                "message": None,
                "recheck_requested": False,
                "trace": self._append_trace(
                    state,
                    "Solver Gate",
                    "approve",
                    "Human approved the candidate solution despite low confidence or re-check request.",
                    output={"next_step": "explain"},
                ),
            }

        if review.get("action") not in {"edit", "recheck"}:
            return {
                "next_step": "solver_gate",
                "message": "Solver review supports approve, edit, recheck, or reject.",
            }

        solver = run_solver(state["route"]["solver"])
        previous_solution = state["solver_output"]["solution"]
        solver_output = solver.solve(
            state["parsed_problem"],
            reviewer_feedback=review.get("feedback"),
        )
        verification = verify_solution(
            state["parsed_problem"]["problem_text"],
            solver_output.solution,
        )

        updates: WorkflowGraphState = {
            "solver_output": solver_output.model_dump(),
            "verification": verification.model_dump(),
            "explanation": None,
            "message": None,
            "recheck_requested": False,
            "trace": self._append_trace(
                state,
                "Solver Gate",
                review["action"],
                "Solver re-ran using human feedback.",
                output={
                    "solution": solver_output.solution,
                    "verification": verification.model_dump(),
                },
            ),
        }

        if review.get("action") == "edit" and review.get("feedback"):
            updates["learning_signals"] = self._append_learning_signal(
                state,
                LearningSignalDraft(
                    stage="solver_review",
                    signal_type="solver_feedback",
                    original_value=previous_solution,
                    corrected_value=solver_output.solution,
                    notes=review["feedback"],
                ),
            )

        if (not verification.is_correct) or (
            verification.confidence < self.VERIFIER_CONFIDENCE_THRESHOLD
        ):
            updates["next_step"] = "solver_gate"
            updates["message"] = (
                "Verifier still marked the answer incorrect or not confident enough. "
                "Approve, edit, or re-check again."
            )
        else:
            updates["next_step"] = "explain"

        return updates

    def _handle_final_review(self, state: WorkflowGraphState, review: dict[str, Any]):
        if review.get("stage") != "final_review":
            return {
                "next_step": "final_gate",
                "message": "Expected review for final_review.",
            }

        action = review.get("action")

        if action == "reject":
            return self._reject(state, "final_review")

        if action == "approve":
            return {
                "next_step": "persist",
                "message": None,
                "final_action": "approve",
                "trace": self._append_trace(
                    state,
                    "Final Review",
                    "approve",
                    "Human approved the final answer.",
                    output={"next_step": "persist"},
                ),
            }

        if action == "recheck":
            return {
                "solver_feedback": review.get("feedback"),
                "solver_output": None,
                "verification": None,
                "explanation": None,
                "recheck_requested": False,
                "next_step": "solve",
                "message": None,
                "trace": self._append_trace(
                    state,
                    "Final Review",
                    "recheck",
                    "Human requested a solver re-check before final approval.",
                    output={"solver_feedback": review.get("feedback")},
                ),
            }

        if action != "edit":
            return {
                "next_step": "final_gate",
                "message": "Final review supports approve, edit, recheck, or reject.",
            }

        if not review.get("feedback"):
            return {
                "next_step": "final_gate",
                "message": "Provide the corrected final solution to save it.",
            }

        corrected_solution = review["feedback"]
        verification = verify_solution(
            state["parsed_problem"]["problem_text"],
            corrected_solution,
        )
        explanation = generate_explanation(
            state["parsed_problem"]["problem_text"],
            corrected_solution,
        )

        return {
            "solver_output": {
                **state["solver_output"],
                "solution": corrected_solution,
            },
            "verification": verification.model_dump(),
            "explanation": explanation.explanation,
            "learning_signals": self._append_learning_signal(
                state,
                LearningSignalDraft(
                    stage="final_review",
                    signal_type="final_solution_correction",
                    original_value=state["solver_output"]["solution"],
                    corrected_value=corrected_solution,
                ),
            ),
            "next_step": "persist",
            "message": None,
            "final_action": "edit",
            "trace": self._append_trace(
                state,
                "Final Review",
                "edit",
                "Human corrected the final solution before saving.",
                output={"solution": corrected_solution},
            ),
        }

    def _needs_input_review(self, state: WorkflowGraphState) -> bool:
        if state.get("input_reviewed"):
            return False

        if (
            state.get("ocr_confidence") is not None
            and state["ocr_confidence"] < self.INPUT_CONFIDENCE_THRESHOLD
        ):
            return True

        if (
            state.get("asr_confidence") is not None
            and state["asr_confidence"] < self.INPUT_CONFIDENCE_THRESHOLD
        ):
            return True

        return False

    def _append_learning_signal(
        self,
        state: WorkflowGraphState,
        signal: LearningSignalDraft,
    ):
        learning_signals = list(state.get("learning_signals", []))
        learning_signals.append(signal.model_dump())
        return learning_signals

    def _append_trace(
        self,
        state: WorkflowGraphState,
        agent: str,
        action: str,
        reason: str,
        output: Any | None = None,
    ):
        trace = list(state.get("trace", []))
        trace.append(
            AgentTraceStep(
                agent=agent,
                action=action,
                reason=reason,
                output=self._serialize_trace_output(output),
            ).model_dump()
        )
        return trace

    def _serialize_trace_output(self, output: Any | None):
        if output is None:
            return None

        if isinstance(output, str):
            return output

        return json.dumps(output, indent=2, ensure_ascii=False)

    def _reject(self, state: WorkflowGraphState, stage: str):
        return {
            "status": "rejected",
            "review_stage": stage,
            "next_step": "end",
            "message": "The workflow was rejected by human review.",
            "trace": self._append_trace(
                state,
                "Human Review",
                "reject",
                f"Human rejected the workflow during {stage}.",
            ),
        }

    def _next_step(self, state: WorkflowGraphState):
        return state["next_step"]
