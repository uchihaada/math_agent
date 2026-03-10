import sys
from pathlib import Path
import os

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import MarkdownHeaderTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

from backend.rag.ingestion_utils import extract_chunk_topics, normalize_knowledge_text

BASE_DIR = Path(__file__).resolve().parents[2]

EXAMPLES_PATH = BASE_DIR / "backend" / "knowledge_base" / "examples"
VECTOR_DB_PATH = BASE_DIR / "backend" / "vector_store_examples"

def ingest_examples():

    # Load all markdown files
    md_files = list(Path(EXAMPLES_PATH).glob("**/*.md"))

    docs = []
    for file_path in md_files:
        loader = TextLoader(str(file_path), encoding="utf-8")
        for doc in loader.load():
            doc.page_content = normalize_knowledge_text(doc.page_content)
            docs.append(doc)

    headers = [
        ("#", "example")
    ]

    splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers)

    chunks = []

    for doc in docs:

        filename = os.path.basename(doc.metadata["source"])

        fallback_topic = filename.replace("_examples.md", "")

        split_docs = splitter.split_text(doc.page_content)

        for chunk in split_docs:
            for topic in extract_chunk_topics(chunk.page_content, fallback_topic):
                chunk_copy = chunk.model_copy(deep=True)
                chunk_copy.metadata["type"] = "example"
                chunk_copy.metadata["topic"] = topic
                chunk_copy.metadata["source"] = "curated"
                chunks.append(chunk_copy)

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    vectordb = FAISS.from_documents(
        chunks,
        embedding=embeddings
    )

    vectordb.save_local(VECTOR_DB_PATH)

    print("Example vector store created")


if __name__ == "__main__":
    ingest_examples()
