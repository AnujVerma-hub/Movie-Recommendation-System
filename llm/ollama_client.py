import requests
from Rag_system.config import OLLAMA_MODEL

OLLAMA_URL = "http://localhost:11434/api/generate"

def ollama_chat(prompt: str)-> str:
    print("PROMPT LENGTH:",len(prompt))

    if len(prompt) > 3000:
        return "[Error] prompt too long for ollama"
    
    payload = {
        "model": "llama3.1:8b-instruct-q4_0",
        "prompt": prompt,
        "stream": False
    }

    response = requests.post(OLLAMA_URL,json=payload,timeout=150)
    print("status:",response.status_code)
    print("Raw:", response.text)
    response.raise_for_status()

    return response.json()["response"]

