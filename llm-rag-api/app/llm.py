import os

import requests
from dotenv import load_dotenv


load_dotenv()

OLLAMA_URL = os.getenv(
    "OLLAMA_URL",
    "http://localhost:11434/api/generate"
)

OLLAMA_MODEL = os.getenv(
    "OLLAMA_MODEL",
    "llama3.2"
)


def generate_answer(
    question: str,
    context: str
) -> str:

    prompt = f"""
You are an employee handbook assistant.

Answer the user's question using ONLY the provided context.

If the answer cannot be found in the context,
say:

"I don't know based on the provided document."

Do not invent information.

Context:
{context}

Question:
{question}

Answer:
"""

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": OLLAMA_MODEL,
            "prompt": prompt,
            "stream": False
        },
        timeout=120
    )

    response.raise_for_status()

    data = response.json()

    return data["response"].strip()