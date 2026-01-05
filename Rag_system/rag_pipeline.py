import faiss 
import numpy as np

import pandas as pd 
import requests
from sentence_transformers import SentenceTransformer
from config import *
OLLAMA_URL = "http://localhost:11434/api/generate"

df = pd.read_csv(DATA_PATH)

embed_model = SentenceTransformer(EMBEDDING_MODEL)
index = faiss.read_index(FAISS_INDEX_PATH)

documents = df.to_dict(orient="records")

def retrive(query, k=TOP_k):
    q_emb = embed_model.encode([query]).astype("float32")
    faiss.normalize_L2(q_emb)

    D, idxs = index.search(q_emb, k)
    return [documents[i] for i in idxs[0] if i < len(documents)]

def format_context(docs):
    chunks = []

    for d in docs:

        if not isinstance(d,dict):
            continue
        chunk = (
            "Title: " + str(d.get("title","N\A")) + "\n"
            "Genres: " + str(d.get("genre","N\A")) + "\n"
            "IMDB Rating: " + str(d.get("imdb_rating","N\A")) + "\n"
            "Available on: " + str(d.get("where_to_watch","N\A")) + "\n"
            "Over-view: " + str(d.get("overview","N\A"))

        )

            
        chunks.append(chunk)

    return "\n\n---\n\n".join(chunks)




def ask_llm(query, context):

    context = context[:3500]

    

    prompt = f"""
You are a movie recommendation assistant.

Use ONLY the context below to answer.
If the answer is not in the context, say "I don't know".

Context:
{context}

User question:
{query}

ANSWER:
"""
    
    payload = {
        "model": "llama3.1",
        "prompt":prompt,
        "stream": False
    }

    response = requests.post(OLLAMA_URL,json=payload)
    response.raise_for_status()

    return response.json()["response"]

def rag_answer(query):
    docs = retrive(query)
    
    context= format_context(docs)
    return ask_llm(query, context)



