from langchain_core.messages import HumanMessage, SystemMessage

from backend.llm.llm import get_llm
from backend.models.schemas import ParserOutput
from backend.utils.llm_json import invoke_json_model
from backend.utils.prompt_template import parser_system_prompt, parser_user_prompt


def parse_question(question: str) -> ParserOutput:
    llm = get_llm()
    messages = [
        SystemMessage(content=parser_system_prompt()),
        HumanMessage(content=parser_user_prompt(question)),
    ]
    return invoke_json_model(
        llm,
        messages,
        ParserOutput,
        (
            "Return a JSON object with exactly these keys: "
            "problem_text (string), topics (array of strings), variables (array of strings), "
            "constraints (array of strings), needs_clarification (boolean)."
        ),
    )
