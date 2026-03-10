import json
import re
from typing import TypeVar

from langchain_core.messages import AIMessage, HumanMessage
from pydantic import BaseModel, ValidationError

ModelT = TypeVar("ModelT", bound=BaseModel)


def content_to_text(content) -> str:
    if isinstance(content, str):
        return content.strip()

    if isinstance(content, list):
        parts = []
        for item in content:
            if isinstance(item, dict):
                parts.append(str(item.get("text", item)))
            else:
                parts.append(str(item))
        return " ".join(parts).strip()

    return str(content).strip()


def extract_json_object(text: str) -> str | None:
    fenced_match = re.search(r"```(?:json)?\s*(\{.*\})\s*```", text, flags=re.DOTALL)
    if fenced_match:
        candidate = fenced_match.group(1).strip()
        try:
            json.loads(candidate)
            return candidate
        except json.JSONDecodeError:
            pass

    first_brace = text.find("{")
    last_brace = text.rfind("}")
    if first_brace == -1 or last_brace == -1 or first_brace >= last_brace:
        return None

    candidate = text[first_brace : last_brace + 1].strip()
    try:
        json.loads(candidate)
        return candidate
    except json.JSONDecodeError:
        return None


def parse_json_model(text: str, model_cls: type[ModelT]) -> ModelT:
    json_blob = extract_json_object(text)
    if json_blob is None:
        raise ValueError("Model response did not contain a valid JSON object.")

    data = json.loads(json_blob)
    return model_cls.model_validate(data)


def invoke_json_model(
    llm,
    messages,
    model_cls: type[ModelT],
    schema_instruction: str,
    *,
    retries: int = 1,
) -> ModelT:
    last_error: Exception | None = None
    working_messages = list(messages)

    for _ in range(retries + 1):
        response = llm.invoke(working_messages)
        text = content_to_text(response.content)
        try:
            return parse_json_model(text, model_cls)
        except (ValueError, ValidationError, json.JSONDecodeError) as exc:
            last_error = exc
            working_messages = [
                *messages,
                AIMessage(content=text),
                HumanMessage(
                    content=(
                        "Return ONLY valid JSON. "
                        f"{schema_instruction} "
                        "Do not include markdown fences or extra explanation."
                    )
                ),
            ]

    raise ValueError(f"Unable to parse JSON model response: {last_error}")
