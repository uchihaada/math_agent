from typing import List, Literal, Optional

from pydantic import BaseModel, Field


class RetrievedContextItem(BaseModel):
    content: str
    source: str
    topic: Optional[str] = None
    doc_type: Optional[str] = None


class AgentTraceStep(BaseModel):
    agent: str
    action: str
    reason: str
    output: Optional[str] = None


class ParserOutput(BaseModel):
    problem_text: str
    topics: List[str]
    variables: List[str]
    constraints: List[str]
    needs_clarification: bool


class RouterOutput(BaseModel):
    solver: str


class SolverOutput(BaseModel):
    solution: str
    retrieved_context: List[RetrievedContextItem] = Field(default_factory=list)


class VerifierOutput(BaseModel):
    is_correct: bool
    confidence: float
    issues: List[str] = Field(default_factory=list)


class ExplanationOutput(BaseModel):
    explanation: str


class LearningSignalDraft(BaseModel):
    stage: str
    signal_type: str
    original_value: Optional[str] = None
    corrected_value: Optional[str] = None
    notes: Optional[str] = None


class HumanReviewInput(BaseModel):
    stage: Literal["input_review", "parser_review", "solver_review", "final_review"]
    action: Literal["approve", "edit", "reject", "recheck"]
    feedback: Optional[str] = None


class SolveRequest(BaseModel):
    input_type: Optional[str] = None
    text: Optional[str] = None
    ocr_confidence: Optional[float] = None
    asr_confidence: Optional[float] = None
    input_reviewed: bool = False
    recheck_requested: bool = False
    thread_id: Optional[str] = None
    review: Optional[HumanReviewInput] = None


class ExtractionResponse(BaseModel):
    input_type: Literal["image", "audio"]
    text: str
    confidence: float
    requires_human_review: bool
    applied_corrections: List[str] = Field(default_factory=list)
    alternatives: List[str] = Field(default_factory=list)


class FeedbackRequest(BaseModel):
    interaction_id: int
    is_correct: bool
    comment: Optional[str] = None
