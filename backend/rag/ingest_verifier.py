import sys
from pathlib import Path
import os

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import MarkdownHeaderTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

from backend.rag.ingestion_utils import normalize_knowledge_text

BASE_DIR = Path(__file__).resolve().parents[2]
VERIFIER_PATH = BASE_DIR / "backend" / "knowledge_base" / "verifier"
VECTOR_DB_PATH = BASE_DIR / "backend" / "vector_store_verifier"


def ingest_verifier():

    md_files = list(VERIFIER_PATH.glob("**/*.md"))

    docs = []

    for file_path in md_files:
        loader = TextLoader(str(file_path), encoding="utf-8")
        for doc in loader.load():
            doc.page_content = normalize_knowledge_text(doc.page_content)
            docs.append(doc)

    headers = [
        ("#", "rule")
    ]

    splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers)

    chunks = []

    for doc in docs:

        filename = os.path.basename(doc.metadata["source"])

        rule_type = filename.replace(".md", "")

        split_docs = splitter.split_text(doc.page_content)

        for chunk in split_docs:

            chunk.metadata["type"] = rule_type
            chunk.metadata["source"] = "verifier"

            chunks.append(chunk)

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    vectordb = FAISS.from_documents(
        chunks,
        embedding=embeddings
    )

    vectordb.save_local(VECTOR_DB_PATH)

    print("Verifier vector store created")


if __name__ == "__main__":
    ingest_verifier()
