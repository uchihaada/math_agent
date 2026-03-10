import json
import re
from difflib import SequenceMatcher

from .database import conn, db_lock, serialize_topic

TOKEN_PATTERN = re.compile(r"[a-z0-9_^]+")
MEMORY_STOPWORDS = {
    "the",
    "and",
    "for",
    "with",
    "from",
    "that",
    "this",
    "then",
    "when",
    "into",
    "over",
    "under",
    "after",
    "before",
    "using",
    "find",
    "evaluate",
    "given",
    "what",
    "show",
    "prove",
    "determine",
    "solve",
}
INTENT_KEYWORDS = {
    "limit": ("lim", "limit", "approach", "approaches"),
    "derivative": ("derivative", "differentiate", "d_dx", "dy_dx"),
    "determinant": ("determinant", "matrix", "det"),
    "integral": ("integral", "integration"),
    "probability": ("probability", "event", "random", "dice", "coin", "bag"),
    "equation": ("equation", "roots", "root"),
    "logarithm": ("log", "ln", "logarithm"),
    "eigen": ("eigenvalue", "eigenvalues", "eigenvector", "eigenvectors"),
}
MIN_MEMORY_SEQUENCE_SIMILARITY = 0.33
MIN_MEMORY_TOKEN_OVERLAP = 0.20


def _serialize_payload(value):
    if value is None or isinstance(value, str):
        return value

    if isinstance(value, (dict, list, tuple)):
        return json.dumps(value)

    return str(value)


def _deserialize_json(value):
    if value is None:
        return None

    if isinstance(value, (dict, list)):
        return value

    try:
        return json.loads(value)
    except (TypeError, json.JSONDecodeError):
        return value


def _normalize_problem_text(text):
    normalized = (text or "").lower()
    normalized = normalized.replace("d/dx", " d_dx ")
    normalized = normalized.replace("dy/dx", " dy_dx ")
    normalized = normalized.replace("dx/dy", " dx_dy ")
    normalized = normalized.replace("→", " -> ")
    normalized = normalized.replace("->", " -> ")
    normalized = normalized.replace("∫", " integral ")
    normalized = normalized.replace("∞", " infinity ")
    return normalized


def _significant_terms(text):
    normalized = _normalize_problem_text(text)
    return {
        token
        for token in TOKEN_PATTERN.findall(normalized)
        if len(token) > 1 and token not in MEMORY_STOPWORDS
    }


def _extract_intent_tags(text):
    normalized = _normalize_problem_text(text)
    terms = _significant_terms(normalized)
    intents = set()

    for intent, keywords in INTENT_KEYWORDS.items():
        if any(keyword in normalized for keyword in keywords):
            intents.add(intent)
            continue

        if any(keyword in terms for keyword in keywords):
            intents.add(intent)

    return intents


def _token_overlap_ratio(query_text, candidate_text):
    query_terms = _significant_terms(query_text)
    candidate_terms = _significant_terms(candidate_text)
    if not query_terms or not candidate_terms:
        return 0.0

    shared_terms = query_terms.intersection(candidate_terms)
    return len(shared_terms) / min(len(query_terms), len(candidate_terms))


def _memory_match_score(problem_text, candidate_text, topics, stored_topics):
    query_text = problem_text or ""
    candidate_text = candidate_text or ""
    if not query_text.strip() or not candidate_text.strip():
        return None

    query_intents = _extract_intent_tags(query_text)
    candidate_intents = _extract_intent_tags(candidate_text)
    if query_intents and candidate_intents and query_intents.isdisjoint(candidate_intents):
        return None

    sequence_similarity = SequenceMatcher(
        None,
        query_text.lower(),
        candidate_text.lower(),
    ).ratio()
    token_overlap = _token_overlap_ratio(query_text, candidate_text)
    if sequence_similarity < MIN_MEMORY_SEQUENCE_SIMILARITY:
        return None
    if token_overlap < MIN_MEMORY_TOKEN_OVERLAP:
        return None

    topic_bonus = len(set(topics or []).intersection(set(stored_topics or [])))
    intent_bonus = len(query_intents.intersection(candidate_intents)) * 0.5
    return topic_bonus + intent_bonus + sequence_similarity + token_overlap


def save_interaction(
    input_type,
    raw_input,
    parsed_problem,
    topic,
    solution,
    explanation,
    confidence
):
    with db_lock:
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO interactions
            (input_type, raw_input, parsed_problem, topic, solution, explanation, confidence)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                input_type,
                raw_input,
                _serialize_payload(parsed_problem),
                serialize_topic(topic),
                solution,
                explanation,
                confidence
            )
        )

        conn.commit()

        return cursor.lastrowid


def save_retrieval(interaction_id, context):
    with db_lock:
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO retrieval_logs
            (interaction_id, retrieved_context)
            VALUES (?, ?)
            """,
            (interaction_id, _serialize_payload(context))
        )

        conn.commit()


def save_feedback(interaction_id, feedback_type, comment=None):
    with db_lock:
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO feedback
            (interaction_id, feedback_type, comment)
            VALUES (?, ?, ?)
            """,
            (interaction_id, feedback_type, comment)
        )

        conn.commit()


def save_learning_signal(
    interaction_id,
    stage,
    signal_type,
    original_value=None,
    corrected_value=None,
    notes=None,
):
    with db_lock:
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO learning_signals
            (interaction_id, stage, signal_type, original_value, corrected_value, notes)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                interaction_id,
                stage,
                signal_type,
                original_value,
                corrected_value,
                notes,
            )
        )

        conn.commit()


def save_verifier_outcome(interaction_id, is_correct, confidence, issues=None):
    with db_lock:
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO verifier_outcomes
            (interaction_id, is_correct, confidence, issues)
            VALUES (?, ?, ?, ?)
            """,
            (
                interaction_id,
                int(bool(is_correct)),
                confidence,
                _serialize_payload(issues or []),
            )
        )

        conn.commit()


def get_learned_correction_rules(limit=25):
    with db_lock:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT original_value, corrected_value, stage
            FROM learning_signals
            WHERE signal_type IN ('transcript_correction', 'parser_clarification')
              AND original_value IS NOT NULL
              AND corrected_value IS NOT NULL
            ORDER BY created_at DESC
            LIMIT ?
            """,
            (limit,),
        )

        return [
            {
                "original": row[0],
                "corrected": row[1],
                "stage": row[2],
            }
            for row in cursor.fetchall()
        ]


def apply_learned_corrections(text, limit=25):
    if not text:
        return text, []

    corrected_text = text
    applied = []

    for rule in get_learned_correction_rules(limit=limit):
        original = rule["original"]
        corrected = rule["corrected"]

        if not original or not corrected or original == corrected:
            continue

        if original in corrected_text:
            corrected_text = corrected_text.replace(original, corrected)
            applied.append(f"{original} -> {corrected}")

    return corrected_text, applied


def find_similar_interactions(problem_text, topics, limit=3):
    with db_lock:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT id, raw_input, parsed_problem, topic, solution, explanation
            FROM interactions
            ORDER BY created_at DESC
            LIMIT 100
            """
        )

        candidates = []
        topics = set(topics or [])

        for interaction_id, raw_input, parsed_problem, topic, solution, explanation in cursor.fetchall():
            parsed = _deserialize_json(parsed_problem) or {}
            stored_topics = _deserialize_json(topic)

            if isinstance(stored_topics, str):
                stored_topics = [stored_topics]

            stored_topics = set(stored_topics or [])
            candidate_text = parsed.get("problem_text") if isinstance(parsed, dict) else raw_input
            candidate_text = candidate_text or raw_input or ""

            score = _memory_match_score(
                problem_text,
                candidate_text,
                topics,
                stored_topics,
            )
            if score is None:
                continue

            candidates.append(
                (
                    score,
                    {
                        "interaction_id": interaction_id,
                        "content": (
                            f"Problem: {candidate_text}\n"
                            f"Solution: {solution}\n"
                            f"Explanation: {explanation}"
                        ),
                        "source": "memory",
                        "topic": next(iter(stored_topics), None),
                        "doc_type": "memory_example",
                    },
                )
            )

        candidates.sort(key=lambda item: item[0], reverse=True)
        return [item[1] for item in candidates[:limit]]


def upsert_workflow_runtime(
    thread_id,
    *,
    status=None,
    current_node=None,
    current_agent=None,
    message=None,
    trace=None,
    retrieved_context=None,
    response=None,
    error=None,
):
    with db_lock:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT status, current_node, current_agent, message, trace, retrieved_context, response, error
            FROM workflow_runtime
            WHERE thread_id = ?
            """,
            (thread_id,),
        )
        existing = cursor.fetchone()

        current_status = status
        current_node_value = current_node
        current_agent_value = current_agent
        current_message = message
        current_trace = trace
        current_retrieved_context = retrieved_context
        current_response = response
        current_error = error

        if existing is not None:
            current_status = existing[0] if current_status is None else current_status
            current_node_value = (
                existing[1] if current_node_value is None else current_node_value
            )
            current_agent_value = (
                existing[2] if current_agent_value is None else current_agent_value
            )
            current_message = existing[3] if current_message is None else current_message
            current_trace = _deserialize_json(existing[4]) if current_trace is None else current_trace
            current_retrieved_context = (
                _deserialize_json(existing[5])
                if current_retrieved_context is None
                else current_retrieved_context
            )
            current_response = (
                _deserialize_json(existing[6]) if current_response is None else current_response
            )
            current_error = existing[7] if current_error is None else current_error

        cursor.execute(
            """
            INSERT INTO workflow_runtime
            (thread_id, status, current_node, current_agent, message, trace, retrieved_context, response, error, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
            ON CONFLICT(thread_id) DO UPDATE SET
                status = excluded.status,
                current_node = excluded.current_node,
                current_agent = excluded.current_agent,
                message = excluded.message,
                trace = excluded.trace,
                retrieved_context = excluded.retrieved_context,
                response = excluded.response,
                error = excluded.error,
                updated_at = CURRENT_TIMESTAMP
            """,
            (
                thread_id,
                current_status or "queued",
                current_node_value,
                current_agent_value,
                current_message,
                _serialize_payload(current_trace or []),
                _serialize_payload(current_retrieved_context or []),
                _serialize_payload(current_response),
                current_error,
            ),
        )

        conn.commit()


def get_workflow_runtime(thread_id):
    with db_lock:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT thread_id, status, current_node, current_agent, message, trace, retrieved_context, response, error
            FROM workflow_runtime
            WHERE thread_id = ?
            """,
            (thread_id,),
        )
        row = cursor.fetchone()
        if row is None:
            return None

        return {
            "thread_id": row[0],
            "status": row[1],
            "current_node": row[2],
            "current_agent": row[3],
            "message": row[4],
            "trace": _deserialize_json(row[5]) or [],
            "retrieved_context": _deserialize_json(row[6]) or [],
            "response": _deserialize_json(row[7]),
            "error": row[8],
        }
