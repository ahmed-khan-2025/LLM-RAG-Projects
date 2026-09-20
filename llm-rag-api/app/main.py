from pathlib import Path

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from .llm import generate_answer
from .rag import RAGSystem


app = FastAPI(
    title="Simple LLM RAG API",
    description="Employee Handbook Question Answering API",
    version="1.0.0"
)


BASE_DIR = Path(__file__).resolve().parent.parent

DOCUMENT_PATH = (
    BASE_DIR
    / "data"
    / "employee_handbook.txt"
)


rag = RAGSystem(
    str(DOCUMENT_PATH)
)


class QuestionRequest(BaseModel):
    question: str


class QuestionResponse(BaseModel):
    question: str
    answer: str
    sources: list[dict]


@app.get("/")
def home():
    return {
        "message": "Simple LLM RAG API is running"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


@app.post(
    "/ask",
    response_model=QuestionResponse
)
def ask_question(request: QuestionRequest):

    question = request.question.strip()

    if not question:
        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty"
        )

    results = rag.search(
        question,
        top_k=3
    )

    context = "\n\n".join(
        result["text"]
        for result in results
    )

    try:
        answer = generate_answer(
            question,
            context
        )

    except Exception as exc:
        raise HTTPException(
            status_code=503,
            detail=f"LLM service unavailable: {exc}"
        )

    return {
        "question": question,
        "answer": answer,
        "sources": results
    }