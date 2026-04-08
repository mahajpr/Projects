from crewai.tools import tool
from sentence_transformers import SentenceTransformer
from pypdf import PdfReader
import faiss
import numpy as np
import os

embed_model = SentenceTransformer("all-MiniLM-L6-v2")


@tool
def load_resume(path: str) -> str:
    """Extract text from resume PDF."""
    reader = PdfReader(path)
    text = ""

    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text

    return text


@tool
def extract_chunks(text: str) -> list:
    """Split resume text into chunks."""
    chunk_size = 200
    return [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]


@tool
def create_embeddings(chunks: list) -> list:
    """Create embeddings for chunks."""
    return embed_model.encode(chunks).tolist()


@tool
def semantic_search(chunks: list, query: str) -> list:
    """Find relevant resume sections for a job description."""

    embeddings = embed_model.encode(chunks)

    dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(np.array(embeddings))

    query_embed = embed_model.encode([query])
    _, indices = index.search(np.array(query_embed), 2)

    return [chunks[i] for i in indices[0]]