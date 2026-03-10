import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from backend.rag.ingestion_utils import canonicalize_topic, extract_chunk_topics


def test_probability_aliases():
    assert canonicalize_topic("probability") == "probability"
    assert canonicalize_topic("statistics") == "probability"
    assert canonicalize_topic("combinatorics") == "probability"
    assert canonicalize_topic("bayes_theorem") == "probability"
    assert canonicalize_topic("conditional_probability") == "probability"
    assert canonicalize_topic("poisson_distribution") == "probability"


def test_algebra_aliases():
    assert canonicalize_topic("algebra") == "algebra"
    assert canonicalize_topic("quadratics") == "algebra"
    assert canonicalize_topic("logarithms") == "algebra"
    assert canonicalize_topic("inequalities") == "algebra"
    assert canonicalize_topic("equations") == "algebra"
    assert canonicalize_topic("complex_numbers") == "algebra"
    assert canonicalize_topic("theory_of_equations") == "algebra"
    assert canonicalize_topic("binomial_theorem") == "algebra"


def test_extract_chunk_topics_normalizes_probability_labels():
    text = """
Problem:
Example probability problem

Topics:
probability, statistics, combinatorics
"""
    topics = extract_chunk_topics(text, "probability")
    assert topics == ["probability"]


if __name__ == "__main__":
    test_probability_aliases()
    test_algebra_aliases()
    test_extract_chunk_topics_normalizes_probability_labels()
    print("ingestion_utils tests passed")
