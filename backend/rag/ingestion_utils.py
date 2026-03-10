from __future__ import annotations

import re


ALLOWED_TOPICS = {
    "calculus",
    "algebra",
    "probability",
    "linear_algebra",
}

TOPIC_ALIASES = {
    "matrix": "linear_algebra",
    "matrices": "linear_algebra",
    "determinant": "linear_algebra",
    "determinants": "linear_algebra",
    "vectors": "linear_algebra",
    "vector": "linear_algebra",
    "inverse_trigonometry": "calculus",
    "inverse_functions": "calculus",
    "derivatives": "calculus",
    "limits": "calculus",
    "trigonometric": "calculus",
    "integration": "calculus",
    "series": "calculus",
    "simple_optimization": "calculus",
    "mean_value_theorems": "calculus",
    "quadratics": "algebra",
    "logarithms": "algebra",
    "inequalities": "algebra",
    "equations": "algebra",
    "complex_numbers": "algebra",
    "theory_of_equations": "algebra",
    "binomial_theorem": "algebra",
    "statistics": "probability",
    "combinatorics": "probability",
    "permutation": "probability",
    "permutations": "probability",
    "combination": "probability",
    "combinations": "probability",
    "conditional_probability": "probability",
    "independent_events": "probability",
    "dependent_events": "probability",
    "law_of_total_probability": "probability",
    "bayes": "probability",
    "bayes_theorem": "probability",
    "random_variable": "probability",
    "expected_value": "probability",
    "expectation": "probability",
    "variance": "probability",
    "binomial": "probability",
    "binomial_distribution": "probability",
    "poisson": "probability",
    "poisson_distribution": "probability",
    "geometrical_probability": "probability",
    "partial_derangement": "probability",
    "derangement": "probability",
    "derangements": "probability",
}

ASCII_REPLACEMENTS = {
    "\u00a0": " ",
    "\u00b1": "+/-",
    "\u00b2": "^2",
    "\u00b3": "^3",
    "\u00b9": "^1",
    "\u03b8": "theta",
    "\u03bb": "lambda",
    "\u0394": "Delta",
    "\u03a3": "Sigma",
    "\u03c0": "pi",
    "\u2013": "-",
    "\u2014": "-",
    "\u2018": "'",
    "\u2019": "'",
    "\u201c": '"',
    "\u201d": '"',
    "\u2026": "...",
    "\u2032": "'",
    "\u207f": "^n",
    "\u2080": "_0",
    "\u2081": "_1",
    "\u2082": "_2",
    "\u2083": "_3",
    "\u2084": "_4",
    "\u2085": "_5",
    "\u2086": "_6",
    "\u2087": "_7",
    "\u2088": "_8",
    "\u2089": "_9",
    "\u2099": "_n",
    "\u2113": "l",
    "\u2192": "->",
    "\u2202": "partial",
    "\u2208": "in",
    "\u2211": "Sigma",
    "\u2212": "-",
    "\u221a": "sqrt",
    "\u221e": "infinity",
    "\u222b": "integral",
    "\u2248": "~",
    "\u2260": "!=",
    "\u2264": "<=",
    "\u2265": ">=",
    "\u2192": "->",
    "\ufeff": "",
}

MOJIBAKE_MARKERS = ("â", "Î", "Ï", "Ã", "Â")


def normalize_knowledge_text(text: str) -> str:
    normalized = text.replace("\r\n", "\n").replace("\r", "\n")

    if any(marker in normalized for marker in MOJIBAKE_MARKERS):
        try:
            repaired = normalized.encode("latin1").decode("utf-8")
        except UnicodeError:
            repaired = normalized
        else:
            if repaired.count("\ufffd") <= normalized.count("\ufffd"):
                normalized = repaired

    for source, target in ASCII_REPLACEMENTS.items():
        normalized = normalized.replace(source, target)

    normalized = re.sub(r"[ \t]+", " ", normalized)
    normalized = re.sub(r"\n{3,}", "\n\n", normalized)
    return normalized.strip()


def canonicalize_topic(raw_topic: str | None) -> str | None:
    if not raw_topic:
        return None

    normalized = raw_topic.strip().lower().replace("-", "_").replace(" ", "_")
    normalized = normalized.strip(" ,")

    if normalized in ALLOWED_TOPICS:
        return normalized

    return TOPIC_ALIASES.get(normalized)


def extract_chunk_topics(text: str, fallback_topic: str) -> list[str]:
    lines = [line.strip() for line in text.splitlines()]
    raw_topics: list[str] = []

    for index, line in enumerate(lines):
        lower_line = line.lower()
        if not (lower_line.startswith("topic:") or lower_line.startswith("topics:")):
            continue

        _, _, tail = line.partition(":")
        candidate = tail.strip()
        if not candidate and index + 1 < len(lines):
            candidate = lines[index + 1].strip()

        raw_topics.extend(part.strip() for part in candidate.split(",") if part.strip())
        break

    topics = []
    for raw_topic in raw_topics:
        canonical = canonicalize_topic(raw_topic)
        if canonical and canonical not in topics:
            topics.append(canonical)

    fallback = canonicalize_topic(fallback_topic) or fallback_topic
    if fallback not in topics:
        topics.append(fallback)

    return topics
