from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI

from app.api.routes import router


BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(
    BASE_DIR / ".env"
)


app = FastAPI(
    title="Advanced Audio RAG Assistant",
    description=(
        "Local audio question-answering system "
        "using Whisper, hybrid retrieval, "
        "reranking and Ollama."
    ),
    version="1.0.0",
)


app.include_router(router)


@app.get("/")
def root():

    return {
        "message": "Advanced Audio RAG Assistant",
        "docs": "/docs",
        "health": "/health",
    }