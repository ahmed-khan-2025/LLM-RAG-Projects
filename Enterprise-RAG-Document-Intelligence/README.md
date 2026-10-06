# Enterprise RAG Document Intelligence

A production-oriented Retrieval-Augmented Generation (RAG) API built with:

- Python
- FastAPI
- PostgreSQL
- pgvector
- Sentence Transformers
- Ollama
- Docker
- pytest

## Architecture

Documents -> Text extraction -> Chunking -> Embeddings -> pgvector
-> Similarity Search -> Retrieved Context -> Ollama LLM -> Answer + Sources

## Features

- PDF, DOCX and TXT ingestion
- Text chunking with overlap
- 384-dimensional sentence-transformer embeddings
- PostgreSQL + pgvector vector storage
- Cosine similarity search
- Ollama local LLM generation
- Source-aware answers
- REST API
- Docker PostgreSQL
- Basic automated test

## Requirements

- Windows 10/11
- Python 3.10 recommended
- Docker Desktop
- Ollama

## 1. Create virtual environment

```powershell
py -3.10 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

If PowerShell blocks activation, run:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

## 2. Start PostgreSQL + pgvector

```powershell
docker compose up -d
```

Check:

```powershell
docker ps
```

You should see:

```text
enterprise-rag-postgres
```

## 3. Start Ollama

Make sure Ollama is installed and running.

Check:

```powershell
ollama list
```

If `llama3.2:latest` is not available:

```powershell
ollama pull llama3.2
```

Test it:

```powershell
ollama run llama3.2
```

Press Ctrl+C when finished.

## 4. Start FastAPI

From the project root:

```powershell
.\.venv\Scripts\Activate.ps1
uvicorn app.main:app --reload
```

Open:

```text
http://127.0.0.1:8000/docs
```

## 5. Upload a document

Use Swagger:

```text
POST /documents/upload
```

Upload a PDF, DOCX or TXT file.

The system:

1. Reads the document
2. Splits it into chunks
3. Creates embeddings
4. Stores chunks and vectors in pgvector

## 6. Ask a question

Use:

```text
POST /chat
```

Example JSON:

```json
{
  "question": "What is the main purpose of this document?",
  "top_k": 5
}
```

The response contains:

- answer
- source document
- similarity score
- retrieved chunk ID

## 7. Test

Run:

```powershell
python -m pytest -v
```

## Important

The first embedding model download can take some time:

```text
sentence-transformers/all-MiniLM-L6-v2
```

It produces 384-dimensional vectors, which matches:

```sql
embedding vector(384)
```

## RAG flow

```text
User question
      |
      v
Question embedding
      |
      v
pgvector cosine similarity
      |
      v
Top-K document chunks
      |
      v
Prompt + retrieved context
      |
      v
Ollama
      |
      v
Grounded answer + sources
```

## Future production improvements

- Reranking
- Hybrid BM25 + vector search
- Document metadata filtering
- Authentication and authorization
- Multi-user document isolation
- RAG evaluation
- Prompt versioning
- Langfuse / MLflow tracing
- Redis caching
- Prometheus metrics
- Grafana dashboard
- Agentic RAG
- CI/CD
- Kubernetes deployment
