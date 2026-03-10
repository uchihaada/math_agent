import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from backend.memory.memory_store import _memory_match_score


def test_memory_match_rejects_cross_intent_examples():
    query = "Evaluate the limit lim x->0 (sin x - x + x^3/6) / x^5"
    candidate = "Find derivative of determinant | x x^2 ; x^3 2x |"
    score = _memory_match_score(query, candidate, {"calculus"}, {"calculus"})
    assert score is None


def test_memory_match_accepts_same_intent_examples():
    query = "Evaluate the limit lim x->0 (sin x - x + x^3/6) / x^5"
    candidate = "Evaluate the limit lim x->0 (sin x - x) / x^3"
    score = _memory_match_score(query, candidate, {"calculus"}, {"calculus"})
    assert score is not None


if __name__ == "__main__":
    test_memory_match_rejects_cross_intent_examples()
    test_memory_match_accepts_same_intent_examples()
    print("memory_store tests passed")
