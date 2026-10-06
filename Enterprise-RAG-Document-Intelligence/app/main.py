from pathlib import Path
import shutil
from fastapi import FastAPI, File, UploadFile, HTTPException
from pydantic import BaseModel

from app.ingestion.loader import load_document
from app.ingestion.chunker import chunk_text
from app.ingestion.embeddings import embed_texts
from app.database.connection import init_db
from app.database.repository import insert_chunks, search_chunks
from app.llm.ollama_client import generate_answer

UPLOAD_DIR = Path("documents")
UPLOAD_DIR.mkdir(exist_ok=True)

app = FastAPI(
    title="Enterprise RAG Document Intelligence",
    version="1.0.0",
    description="RAG API using FastAPI, PostgreSQL/pgvector, sentence-transformers and Ollama."
)

@app.on_event("startup")
def startup():
    init_db()

class ChatRequest(BaseModel):
    question: str
    top_k: int = 5

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/documents/upload")
async def upload_document(file: UploadFile = File(...)):
    allowed = {".pdf", ".docx", ".txt"}
    suffix = Path(file.filename or "").suffix.lower()
    if suffix not in allowed:
        raise HTTPException(status_code=400, detail="Only PDF, DOCX and TXT files are supported.")

    destination = UPLOAD_DIR / Path(file.filename).name
    with destination.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        text = load_document(destination)
        chunks = chunk_text(text)

        if not chunks:
            raise HTTPException(status_code=400, detail="No readable text found in the document.")

        embeddings = embed_texts(chunks)
        count = insert_chunks(destination.name, chunks, embeddings)

        return {
            "filename": destination.name,
            "chunks_created": count,
            "message": "Document indexed successfully."
        }
    except Exception as exc:
        if destination.exists():
            destination.unlink(missing_ok=True)
        raise HTTPException(status_code=500, detail=str(exc))

@app.post("/chat")
def chat(request: ChatRequest):
    if not request.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty.")

    query_embedding = embed_texts([request.question])[0]
    results = search_chunks(query_embedding, max(1, min(request.top_k, 10)))

    if not results:
        return {
            "answer": "I don't have enough information in the indexed documents to answer that.",
            "sources": []
        }

    context_parts = []
    sources = []

    for index, result in enumerate(results, start=1):
        context_parts.append(
            f"[Source {index}]\n"
            f"Document: {result['filename']}\n"
            f"Similarity: {result['similarity']:.4f}\n"
            f"Content:\n{result['content']}"
        )
        sources.append({
            "filename": result["filename"],
            "similarity": round(result["similarity"], 4),
            "chunk_id": result["id"]
        })

    context = "\n\n".join(context_parts)
    answer = generate_answer(request.question, context)

    return {
        "answer": answer,
        "sources": sources
    }
