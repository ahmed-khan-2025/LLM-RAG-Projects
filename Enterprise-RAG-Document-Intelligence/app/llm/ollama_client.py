import os
import requests

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434/api/generate")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2:latest")

SYSTEM_INSTRUCTION = """
You are an enterprise document question-answering assistant.

Rules:
1. Answer using only the supplied context.
2. Do not invent facts.
3. If the context does not contain enough information, say:
   "I don't have enough information in the provided documents."
4. Give a concise, clear answer.
5. Mention the relevant document name when useful.
"""

def generate_answer(question: str, context: str) -> str:
    prompt = f"""
{SYSTEM_INSTRUCTION}

CONTEXT:
{context}

QUESTION:
{question}

ANSWER:
"""

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": OLLAMA_MODEL,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.1
            }
        },
        timeout=180
    )
    response.raise_for_status()
    data = response.json()
    return data.get("response", "").strip()
