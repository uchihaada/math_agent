from collections.abc import Mapping

from backend.models.schemas import ParserOutput, SolverOutput
from backend.llm.llm import get_llm
from backend.rag.retriever import retrieve_context
from backend.utils.prompt_template import base_solver_prompt, base_solver_user_prompt
from langchain_core.messages import SystemMessage, HumanMessage


def _read_problem_field(parsed_problem: ParserOutput | Mapping[str, object], field: str):
    if isinstance(parsed_problem, ParserOutput):
        return getattr(parsed_problem, field)

    return parsed_problem[field]


class BaseSolver:

    def __init__(self, domain_prompt):
        self.system_prompt = base_solver_prompt() + "\n" + domain_prompt
        self.llm = get_llm()

    def retrieve(self, parsed_problem: ParserOutput | Mapping[str, object]):
        query = _read_problem_field(parsed_problem, "problem_text")
        topics = _read_problem_field(parsed_problem, "topics")
        context = retrieve_context(query, topics)
        return context["formulas"], context["examples"], context["sources"]

    def solve(
        self,
        parsed_problem: ParserOutput | Mapping[str, object],
        reviewer_feedback: str | None = None,
    ) -> SolverOutput:

        problem = _read_problem_field(parsed_problem, "problem_text")
        formulas, examples, sources = self.retrieve(parsed_problem)

        messages = [
            SystemMessage(content=self.system_prompt),
            HumanMessage(content=base_solver_user_prompt(problem, formulas, examples))
        ]

        if reviewer_feedback:
            messages.append(
                HumanMessage(
                    content=(
                        "Reviewer feedback for this re-check: "
                        f"{reviewer_feedback}\nIncorporate it before finalizing the solution."
                    )
                )
            )

        response = self.llm.invoke(messages)

        return SolverOutput(
            solution=response.content,
            retrieved_context=sources,
        )
