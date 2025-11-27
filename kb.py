import os
import uuid

import chromadb
from chromadb.utils import embedding_functions
from pypdf import PdfReader

# We don't need any API key for embeddings now.
# We'll use a local SentenceTransformer model:
# "all-MiniLM-L6-v2" - small, fast, good enough for semantic search.

# Create / connect to persistent ChromaDB
chroma_client = chromadb.PersistentClient(path="chroma_db")

# SentenceTransformer-based embedding function (runs locally)
embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
)

# Collection to store document chunks
collection = chroma_client.get_or_create_collection(
    name="company_kb_local",
    embedding_function=embedding_fn,
)


def _chunk_text(text: str, chunk_size: int = 800, overlap: int = 200):
    """
    Split long text into overlapping chunks so embeddings work better.
    """
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        start += chunk_size - overlap
    return chunks


def add_pdf_to_kb(file_path: str, source_name: str) -> int:
    """
    Read a PDF file, extract text, split into chunks, and add to ChromaDB.
    """
    reader = PdfReader(file_path)
    full_text = ""
    for page in reader.pages:
        page_text = page.extract_text() or ""
        full_text += page_text + "\n"

    return add_text_to_kb(full_text, source_name)


def add_text_to_kb(text: str, source_name: str) -> int:
    """
    Add plain text to the knowledge base as multiple chunks.
    """
    if not text.strip():
        return 0

    chunks = _chunk_text(text)
    ids = [str(uuid.uuid4()) for _ in chunks]
    metadatas = [{"source": source_name} for _ in chunks]

    collection.add(
        ids=ids,
        documents=chunks,
        metadatas=metadatas,
    )

    return len(chunks)


def query_kb(question: str, k: int = 4):
    """
    Retrieve top-k relevant chunks from the KB using semantic search.
    """
    if collection.count() == 0:
        return []

    results = collection.query(
        query_texts=[question],
        n_results=k,
    )

    docs = results.get("documents", [[]])[0]
    metas = results.get("metadatas", [[]])[0]

    contexts = []
    for doc, meta in zip(docs, metas):
        contexts.append(
            {
                "text": doc,
                "source": meta.get("source", "unknown"),
            }
        )
    return contexts
