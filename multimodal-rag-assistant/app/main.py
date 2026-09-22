from pathlib import Path

from dotenv import load_dotenv


BASE_DIR = Path(
    __file__
).resolve().parent.parent

load_dotenv(
    BASE_DIR / ".env"
)


from fastapi import FastAPI

from app.api.routes import router


app = FastAPI(
    title="Multimodal RAG Assistant",
    description=(
        "Advanced local video RAG system "
        "using Whisper, vision models, "
        "hybrid retrieval, reranking "
        "and Ollama."
    ),
    version="1.0.0",
)


app.include_router(router)


@app.get("/")
def root():

    return {
        "message": (
            "Multimodal RAG Assistant"
        ),
        "docs": "/docs",
        "health": "/health",
    }