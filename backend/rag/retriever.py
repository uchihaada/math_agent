from pathlib import Path
import re

from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document

from backend.memory.memory_store import find_similar_interactions

# Get absolute paths based on this module's location
module_dir = Path(__file__).parent.parent.parent
knowledge_db_path = module_dir / "backend" / "vector_store_knowledge"
example_db_path = module_dir / "backend" / "vector_store_examples"
verifier_db_path = module_dir / "backend" / "vector_store_verifier"

_embeddings = None

_vector_stores = {
    "knowledge": None,
    "example": None,
    "verifier": None,
}

# FAISS returns L2 distances — lower means more similar.
# Docs with a score above these thresholds are considered irrelevant and dropped.
# Formulas are kept at a looser threshold since a broadly related formula is still useful.
# Examples need to be structurally closer to the query to avoid noise.
FORMULA_SCORE_THRESHOLD = 1.0
EXAMPLE_SCORE_THRESHOLD = 0.65


def _query_terms(text: str):
    return {
        token
        for token in re.findall(r"[a-z0-9_^]+", text.lower())
        if len(token) > 1
    }


def _doc_rank(query_terms: set[str], doc: Document, faiss_score: float = 0.0):
    """
    Composite rank: token overlap + problem-prefix bonus, minus a penalty
    proportional to FAISS L2 distance so semantic similarity is preserved.
    """
    content = doc.page_content.lower()
    token_score = sum(1 for term in query_terms if term in content)
    if "problem:" in content:
        token_score += 3
    # Scale FAISS distance penalty so it's comparable to token scores.
    # A score of 0.5 penalises ~2.5 points; 1.0 penalises ~5 points.
    return token_score - (faiss_score * 5)


def _dedupe_documents(docs_with_scores: list[tuple[Document, float]]):
    """
    Deduplicates by (source, content) — intentionally ignores 'type' so that
    the same text ingested under different type labels (e.g. 'example' vs
    'memory_example') is treated as one entry.
    """
    seen = set()
    unique = []

    for doc, score in docs_with_scores:
        key = (
            doc.metadata.get("source"),
            doc.page_content.strip(),
        )
        if key in seen:
            continue
        seen.add(key)
        unique.append((doc, score))

    return unique


def _serialize_doc(doc: Document):
    return {
        "content": doc.page_content,
        "source": doc.metadata.get("source", "curated"),
        "topic": doc.metadata.get("topic"),
        "doc_type": doc.metadata.get("type"),
    }


def _load_vector_store(path: Path):
    if not path.exists():
        return None

    return FAISS.load_local(
        str(path),
        _get_embeddings(),
        allow_dangerous_deserialization=True,
    )


def _get_embeddings():
    global _embeddings

    if _embeddings is None:
        _embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )

    return _embeddings


def _get_vector_store(name: str):
    if _vector_stores[name] is not None:
        return _vector_stores[name]

    if name == "knowledge":
        _vector_stores[name] = _load_vector_store(knowledge_db_path)
    elif name == "example":
        _vector_stores[name] = _load_vector_store(example_db_path)
    else:
        _vector_stores[name] = _load_vector_store(verifier_db_path)

    return _vector_stores[name]


def retrieve_context(query, topics):
    knowledge_db = _get_vector_store("knowledge")
    example_db = _get_vector_store("example")
    query_terms = _query_terms(query)

    raw_formula_docs: list[tuple[Document, float]] = []
    raw_example_docs: list[tuple[Document, float]] = []

    for topic in topics:
        if knowledge_db is not None:
            results = knowledge_db.similarity_search_with_score(
                query, k=7, filter={"topic": topic}
            )
            raw_formula_docs.extend(
                (doc, score) for doc, score in results
                if score < FORMULA_SCORE_THRESHOLD
            )

        if example_db is not None:
            results = example_db.similarity_search_with_score(
                query, k=7, filter={"topic": topic}
            )
            raw_example_docs.extend(
                (doc, score) for doc, score in results
                if score < EXAMPLE_SCORE_THRESHOLD
            )

    formula_docs = sorted(
        _dedupe_documents(raw_formula_docs),
        key=lambda pair: _doc_rank(query_terms, pair[0], pair[1]),
        reverse=True,
    )
    example_docs = sorted(
        _dedupe_documents(raw_example_docs),
        key=lambda pair: _doc_rank(query_terms, pair[0], pair[1]),
        reverse=True,
    )

    formulas = [_serialize_doc(doc) for doc, _ in formula_docs]
    examples = [_serialize_doc(doc) for doc, _ in example_docs]

    # Merge memory examples, skipping anything already present by content
    memory_examples = find_similar_interactions(query, topics, limit=1)
    seen_contents = {item["content"].strip() for item in examples}
    for item in memory_examples:
        content = item.get("content", "").strip()
        if content and content not in seen_contents:
            examples.append(item)
            seen_contents.add(content)

    return {
        "formulas": formulas,
        "examples": examples,
        "sources": formulas + examples,
    }


def retrieve_verifier_rules(problem):
    verifier_db = _get_vector_store("verifier")

    if verifier_db is None:
        return []

    docs = verifier_db.similarity_search(problem, k=3)
    return [doc.page_content for doc in docs]


def append_example_to_vector_store(problem, solution, topics, source="human_approved"):
    if not topics:
        return

    documents = [
        Document(
            page_content=(
                "# Example\n"
                f"Problem: {problem}\n"
                f"Solution: {solution}"
            ),
            metadata={
                "type": "example",
                "topic": topic,
                "source": source,
            },
        )
        for topic in topics
    ]

    example_db = _get_vector_store("example")

    if example_db is None:
        example_db = FAISS.from_documents(documents, embedding=_get_embeddings())
    else:
        example_db.add_documents(documents)

    example_db.save_local(str(example_db_path))
    _vector_stores["example"] = example_db