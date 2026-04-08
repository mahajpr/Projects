import numpy as np
import os
from fastapi import APIRouter
from pydantic import BaseModel
from groq import Groq
from sentence_transformers import SentenceTransformer 
import faiss
from pypdf import PdfReader
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()

API_KEY = os.getenv("GROQ_API_KEY")

if not API_KEY:
    raise ValueError("GROQ_API_KEY is not set")

client = Groq(api_key=API_KEY)

embed_model = SentenceTransformer("all-MiniLM-L6-v2")

class ChatRequest(BaseModel):
    query: str


def load_chunks(text, source, chunk_size=300):
    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunk_text = text[start:end]

        chunks.append({
            "text": chunk_text,
            "source": source
        })

        start = end

    return chunks


def load_file(file):
    if file.endswith(".pdf"):
        reader = PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""
        return text

    elif file.endswith(".txt"):
        with open(file, "r", encoding="utf-8") as f:
            return f.read()

    return ""

def prepare_chunks():
    file_path = "services/rules.txt"   
    text = load_file(file_path)
    chunks = load_chunks(text, "rules.txt")
    return chunks


def create_index(chunks):
    texts = [chunk["text"] for chunk in chunks]

    embeddings = embed_model.encode(texts)

    if len(embeddings.shape) == 1:
        embeddings = embeddings.reshape(1, -1)

    dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(np.array(embeddings))

    return index, embeddings


def search(chunks, query, index, top_k=2):
    query_embed = embed_model.encode([query])

    distances, indices = index.search(np.array(query_embed), top_k)

    results = []
    for i in indices[0]:
        results.append(chunks[i])

    return results


def generate_answer(query, context):
    prompt = f"""
You are the official assistant for an Inter-College Technical Fest.

Your job:
- Answer ONLY using the context provided 
- Do not invent information
- If answer not in context → say:
  "Please contact the event coordinator for this information."

Instructions:
- Be short and clear
- Use bullet points if needed
- Mention rules clearly
- Mention team size if relevant
- Mention time/venue if asked

Context:
{context}

Question:
{query}
"""

    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
    )

    return completion.choices[0].message.content


chunks = prepare_chunks()
index, embeddings = create_index(chunks)


def rag_chat(query):
    results = search(chunks, query, index)

    context = "\n".join([r["text"] for r in results])

    answer = generate_answer(query, context)

    return answer

@router.post("/chat")
def chat_api(req: ChatRequest):
    answer = rag_chat(req.query)
    return {"answer": answer}