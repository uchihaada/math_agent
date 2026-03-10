import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from backend.agents.extraction_agent import _looks_like_noisy_math_ocr, _normalize_math_ocr_text


def main():
    limit_ocr = "Evaluate lim x+0 sinx-x+x3/6 x5"
    assert _normalize_math_ocr_text(limit_ocr) == "Evaluate lim x->0 sin x - x + x^3 / 6 x^5"

    exp_ocr = "Evaluate lim I+0 e z - 1 - x - x2/2 x3"
    normalized = _normalize_math_ocr_text(exp_ocr)
    assert normalized.startswith("Evaluate lim x->0 e^x - 1 - x - x^2 / 2 x^3")
    assert _looks_like_noisy_math_ocr(normalized) is True

    repaired = "Evaluate the limit lim x->0 (e^x - 1 - x - x^2 / 2) / x^3"
    assert _looks_like_noisy_math_ocr(repaired) is False

    print("extraction_agent_ok")


if __name__ == "__main__":
    main()
