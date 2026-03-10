from langchain_core.messages import HumanMessage, SystemMessage

from backend.llm.llm import get_llm
from backend.models.schemas import VerifierOutput
from backend.rag.retriever import retrieve_verifier_rules
from backend.utils.llm_json import invoke_json_model
from backend.utils.prompt_template import verifier_system_prompt, verifier_user_prompt


def verify_solution(problem, solution):
    rules = retrieve_verifier_rules(problem)
    llm = get_llm()
    messages = [
        SystemMessage(content=verifier_system_prompt()),
        HumanMessage(
            content=verifier_user_prompt(
                problem,
                solution,
                rules
            )
        ),
    ]
    return invoke_json_model(
        llm,
        messages,
        VerifierOutput,
        (
            "Return a JSON object with exactly these keys: "
            "is_correct (boolean), confidence (number from 0 to 1), issues (array of strings)."
        ),
    )
