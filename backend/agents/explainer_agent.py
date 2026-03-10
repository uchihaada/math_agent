from langchain_core.messages import HumanMessage, SystemMessage

from backend.llm.llm import get_llm
from backend.models.schemas import ExplanationOutput
from backend.utils.llm_json import content_to_text
from backend.utils.prompt_template import explainer_system_prompt, explainer_user_prompt


def generate_explanation(problem, solution):
    llm = get_llm()
    messages = [
        SystemMessage(content=explainer_system_prompt()),
        HumanMessage(
            content=explainer_user_prompt(
                problem,
                solution
            )
        ),
    ]
    response = llm.invoke(messages)
    return ExplanationOutput(explanation=content_to_text(response.content))
