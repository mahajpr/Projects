from dotenv import load_dotenv
import os
from groq import Groq
import numpy as np

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def load_chunks(text , source , chunk_size =200):
    chunks=[]
    for i in range(0 , len(text),chunk_size):
        chunks.append({
            "text":text[i:i+chunk_size],
            "source":source
        })
    return chunks

def load_folders(folder_path="reviews"):
    all_chunks=[]
    for file in  os.listdir(folder_path):
        if file.endswith(".txt"):
            with open(os.path.join(folder_path, file), "r", encoding="utf-8") as f:
                text = f.read().strip()
                chunks = load_chunks(text, file)
                all_chunks.extend(chunks)
    return all_chunks



def response(query,context):
    context_data = ""
    for data in context:
        context_data = context_data + data['text'] + "\n"
        context_data = context_data + data["source"] + "\n\n"
    prompt = f"""
    Answer only from the following context
    context: {context_data}
    input: {query}
    """
    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
        {
            "role": "user",
            "content": prompt
        }
        ],
    )
    return completion.choices[0].message.content


def get_rag_context(review_text):
    chunks = load_folders()
    if not chunks:
        return []
    matched = []
    for chunk in chunks:
        if review_text.lower() in chunk["text"].lower():
            matched.append(chunk)

    if not matched:
        return chunks[:5]
    return matched[:5]

