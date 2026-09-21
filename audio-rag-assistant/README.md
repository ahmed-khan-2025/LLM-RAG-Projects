# Audio RAG Assistant

A local **Audio Retrieval-Augmented Generation (RAG) Assistant** that converts audio into searchable text, stores semantic representations in a vector database, retrieves relevant information, and generates grounded answers using a local LLM through Ollama.

The project is designed as a practical AI/backend application using **Python, FastAPI, Whisper, Sentence Transformers, ChromaDB, and Ollama**.

---

## Features

* 🎤 Audio-to-text transcription using Whisper
* ⏱️ Timestamped transcription
* 🧩 Intelligent text chunking
* 🧠 Semantic embeddings
* 🔎 Vector similarity search
* 🤖 Local LLM inference with Ollama
* 📚 Retrieval-Augmented Generation
* 📍 Source timestamps in answers
* ⚡ FastAPI REST API
* 📖 Automatic Swagger/OpenAPI documentation
* 🧪 Pytest test suite
* 🔐 Local-first architecture
* 🐳 Docker-ready
* 🔌 Provider-independent LLM architecture

---

## Architecture

```text
                    AUDIO FILE
                        │
                        ▼
                 Whisper / STT
                        │
                        ▼
             Timestamped Transcript
                        │
                        ▼
                    Chunking
                        │
                        ▼
                  Embeddings
                        │
                        ▼
                    ChromaDB
                        │
                        │
              ┌─────────┘
              │
              ▼
           User Question
              │
              ▼
         Query Embedding
              │
              ▼
        Similarity Search
              │
              ▼
       Relevant Audio Chunks
              │
              ▼
        Context Construction
              │
              ▼
           Ollama LLM
              │
              ▼
       Grounded Answer
              │
              ▼
       Answer + Timestamp
```

---

## Technology Stack

| Component            | Technology            |
| -------------------- | --------------------- |
| Programming Language | Python                |
| API Framework        | FastAPI               |
| Speech-to-Text       | Faster-Whisper        |
| Embeddings           | Sentence Transformers |
| Vector Database      | ChromaDB              |
| LLM                  | Ollama                |
| Default LLM          | Llama 3.2             |
| Audio Processing     | FFmpeg                |
| Testing              | Pytest                |
| API Documentation    | Swagger / OpenAPI     |
| Containerization     | Docker                |

---

## Project Structure

```text
audio-rag-assistant/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   │
│   ├── api/
│   │   ├── __init__.py
│   │   └── routes.py
│   │
│   ├── audio/
│   │   ├── __init__.py
│   │   └── transcriber.py
│   │
│   ├── rag/
│   │   ├── __init__.py
│   │   ├── chunker.py
│   │   ├── embeddings.py
│   │   ├── vector_store.py
│   │   └── rag_service.py
│   │
│   ├── llm/
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── ollama.py
│   │   └── factory.py
│   │
│   └── schemas/
│       ├── __init__.py
│       └── chat.py
│
├── data/
│   ├── audio/
│   └── chroma/
│
├── tests/
│   ├── __init__.py
│   ├── test_chunker.py
│   └── test_api.py
│
├── .env
├── .env.example
├── .gitignore
├── requirements.txt
├── Dockerfile
└── README.md
```

---

# How the System Works

## 1. Audio Upload

The user uploads an audio file such as:

```text
meeting.mp3
```

Supported formats can include:

```text
.mp3
.wav
.m4a
.ogg
.flac
```

---

## 2. Speech-to-Text

The audio is processed by Faster-Whisper.

Example:

```text
Audio
  ↓
Whisper
  ↓
Transcript
```

The transcription also contains timestamps.

Example:

```text
00:00 - 00:08
Welcome to today's project meeting.

00:08 - 00:18
Today we are going to discuss the project budget.

00:18 - 00:28
The current budget is one hundred thousand euros.
```

---

## 3. Chunking

The transcript is divided into smaller pieces.

For example:

```text
Chunk 1
"Welcome to today's project meeting."

Chunk 2
"Today we are going to discuss the project budget."

Chunk 3
"The current budget is one hundred thousand euros."
```

Each chunk keeps its timestamp.

---

## 4. Embeddings

Each chunk is converted into a numerical vector using a Sentence Transformer model.

```text
Text
 ↓
Embedding Model
 ↓
Vector
```

For example:

```text
"The project budget is 100000 EUR."

        ↓

[0.021, -0.182, 0.442, ...]
```

---

## 5. Vector Database

The embeddings are stored in ChromaDB.

The database stores information such as:

```text
ID
Text
Embedding
Source
Start timestamp
End timestamp
```

This allows the system to search for information based on **meaning**, not only exact keywords.

---

# 6. User Question

The user can ask:

```text
What is the project budget?
```

The question is converted into an embedding.

```text
Question
   ↓
Embedding
   ↓
Vector Search
```

---

# 7. Retrieval

ChromaDB searches for the most relevant transcript chunks.

For example:

```text
Question:
What is the project budget?

Retrieved:

00:18 - 00:28
"The current budget is one hundred thousand euros."
```

---

# 8. RAG Prompt

The retrieved information is provided to the LLM as context.

Conceptually:

```text
System:
Answer only using the provided context.

Context:
The current budget is one hundred thousand euros.

Question:
What is the project budget?
```

---

# 9. Local LLM

Ollama generates the final answer.

Example:

```text
The current project budget is €100,000.
```

The answer can also include the relevant timestamp.

```text
The current project budget is €100,000.

Source: 00:18 - 00:28
```

---

# Local LLM Architecture

The application uses an abstraction layer around the LLM.

```text
             LLM Interface
                   │
          ┌────────┴────────┐
          │                 │
       Ollama            Future
                         Providers
```

The initial implementation uses Ollama:

```text
FastAPI
   ↓
RAG Service
   ↓
LLM Interface
   ↓
Ollama
   ↓
Llama 3.2
```

This makes it possible to add other providers later without changing the RAG service.

---

# Requirements

Recommended Python versions:

```text
Python 3.10
Python 3.11
```

Python 3.10/3.11 is recommended because some machine-learning libraries may have compatibility issues with newer Python versions.

---

# Installation

## 1. Clone the repository

```bash
git clone <your-repository-url>
cd audio-rag-assistant
```

---

## 2. Create virtual environment

For Python 3.10:

```bash
py -3.10 -m venv .venv
```

Activate it on Windows Git Bash:

```bash
source .venv/Scripts/activate
```

Verify:

```bash
python --version
```

---

## 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

# FFmpeg

FFmpeg is required for audio processing.

Check:

```bash
ffmpeg -version
```

If FFmpeg is installed correctly, the command should display its version information.

---

# Ollama

Install and start Ollama.

Verify:

```bash
ollama list
```

Pull the default model:

```bash
ollama pull llama3.2
```

Test it:

```bash
ollama run llama3.2
```

Exit:

```text
/bye
```

---

# Environment Variables

Create a `.env` file:

```env
LLM_PROVIDER=ollama

OLLAMA_URL=http://localhost:11434
OLLAMA_MODEL=llama3.2

EMBEDDING_MODEL=all-MiniLM-L6-v2

CHROMA_PATH=data/chroma

TOP_K=3
```

The `.env` file should not be committed to Git.

Use `.env.example` as the template.

---

# Running the Application

Start FastAPI:

```bash
uvicorn app.main:app --reload
```

The application will run at:

```text
http://127.0.0.1:8000
```

---

# Swagger Documentation

Open:

```text
http://127.0.0.1:8000/docs
```

Swagger provides an interactive interface for testing the API.

Alternative documentation:

```text
http://127.0.0.1:8000/redoc
```

---

# API Endpoints

## Health Check

```http
GET /health
```

Example response:

```json
{
  "status": "ok"
}
```

---

## Upload Audio

```http
POST /audio/upload
```

Example:

```text
audio file
    ↓
FastAPI
    ↓
Whisper
    ↓
Transcript
    ↓
Chunking
    ↓
Embeddings
    ↓
ChromaDB
```

---

## Ask a Question

```http
POST /chat
```

Request:

```json
{
  "question": "What is the project budget?"
}
```

Example response:

```json
{
  "question": "What is the project budget?",
  "answer": "The project budget is €100,000.",
  "sources": [
    {
      "text": "The current budget is one hundred thousand euros.",
      "score": 0.89,
      "start": 18.0,
      "end": 28.0
    }
  ]
}
```

---

# Example Workflow

Suppose we have:

```text
data/audio/company_meeting.mp3
```

The audio contains:

```text
"Welcome to the project meeting.

The project budget is 100,000 euros.

The development deadline is December 15th."
```

The user asks:

```text
What is the project budget?
```

The RAG system retrieves:

```text
"The project budget is 100,000 euros."
```

The LLM produces:

```text
The project budget is €100,000.
```

The system can also provide:

```text
Timestamp:
00:08 - 00:15
```

---

# Testing

Run the complete test suite:

```bash
python -m pytest -v
```

Run a specific test:

```bash
python -m pytest tests/test_chunker.py -v
```

Run API tests:

```bash
python -m pytest tests/test_api.py -v
```

---

# RAG Pipeline

The complete pipeline is:

```text
                AUDIO
                  │
                  ▼
             Faster-Whisper
                  │
                  ▼
        Timestamped Transcript
                  │
                  ▼
               Chunking
                  │
                  ▼
              Embeddings
                  │
                  ▼
               ChromaDB
                  │
                  │
                  ▼
              User Query
                  │
                  ▼
             Query Embedding
                  │
                  ▼
           Similarity Search
                  │
                  ▼
            Relevant Chunks
                  │
                  ▼
             RAG Prompt
                  │
                  ▼
             Ollama / LLM
                  │
                  ▼
           Grounded Answer
                  │
                  ▼
         Answer + Sources
```

---

# Why RAG?

A normal LLM answers questions from information contained in its model.

RAG adds external information:

```text
User Question
      │
      ▼
Retrieve relevant information
      │
      ▼
Provide information to LLM
      │
      ▼
Generate grounded answer
```

This reduces the need for the LLM to rely on its general knowledge when answering questions about the uploaded audio.

---

# Why Vector Search?

Keyword search might fail when the user uses different words.

For example, the transcript says:

```text
"The company allocates €1,000 annually
for professional development."
```

The user asks:

```text
How much money can employees use for training?
```

There may not be an exact keyword match.

Semantic embeddings can identify that the two pieces of text have similar meaning.

---

# Current Architecture

The current project uses:

```text
Speech-to-Text
        +
Embeddings
        +
Vector Database
        +
RAG
        +
Local LLM
```

This is a practical **RAG application**, rather than simply sending the entire transcript directly to an LLM.

---

# Advanced RAG Extensions

The project can be extended with several advanced techniques.

## Hybrid Search

Combine:

```text
Vector Search
      +
BM25 Keyword Search
```

This can improve retrieval when exact terms and semantic meaning are both important.

---

## Reranking

Instead of immediately sending retrieved documents to the LLM:

```text
Vector Search
      ↓
Candidate Documents
      ↓
CrossEncoder
      ↓
Top Relevant Documents
      ↓
LLM
```

This provides an additional relevance-ranking stage.

---

## Speaker Diarization

Add speaker identification:

```text
Audio
 ↓
Speaker Diarization
 ↓
Speaker 1
Speaker 2
Speaker 3
 ↓
Whisper
```

Then the system can answer questions such as:

```text
What did Speaker 2 say about the project?
```

---

# Future Video Support

The audio RAG system can be extended into a multimodal RAG system.

```text
                    VIDEO
                      │
             ┌────────┴────────┐
             │                 │
             ▼                 ▼
           AUDIO             FRAMES
             │                 │
             ▼                 ▼
         Whisper           Vision Model
             │                 │
             ▼                 ▼
       Transcript       Visual Description
             │                 │
             └────────┬────────┘
                      ▼
                Multimodal RAG
                      │
                      ▼
                  Ollama LLM
                      │
                      ▼
             Answer + Timestamp
```

This would allow questions such as:

```text
What did the presenter say about the machine?
```

and:

```text
What was displayed on the screen?
```

and eventually:

```text
What did the presenter say about the machine,
and what was shown on the screen at that time?
```

---

# Future Improvements

Planned improvements include:

* [ ] Hybrid vector + BM25 retrieval
* [ ] CrossEncoder reranking
* [ ] Speaker diarization
* [ ] Multiple audio files
* [ ] Metadata filtering
* [ ] Better timestamp handling
* [ ] Confidence thresholds
* [ ] Conversation memory
* [ ] Video ingestion
* [ ] Video frame extraction
* [ ] Vision-language models
* [ ] Multimodal retrieval
* [ ] Background processing
* [ ] Docker deployment
* [ ] CI/CD with GitHub Actions
* [ ] Production logging
* [ ] Authentication
* [ ] File-size limits
* [ ] Async processing for long audio

---

# Project Goals

This project demonstrates practical experience with:

* Python backend development
* FastAPI
* REST APIs
* Speech-to-text
* Natural Language Processing
* Embeddings
* Vector databases
* Retrieval-Augmented Generation
* LLM integration
* Local AI inference
* Semantic search
* Software architecture
* Automated testing
* Docker
* AI application development

---

# Example Interview Explanation

A simple way to explain the project:

> I built a local audio RAG system that converts audio into timestamped text using Whisper, chunks and embeds the transcript, stores the embeddings in ChromaDB, retrieves relevant information for a user's question, and sends the retrieved context to a local LLM through Ollama. The system returns a grounded answer together with source information and timestamps. The architecture is provider-independent so the LLM layer can be replaced without changing the core RAG pipeline.

---

# License

This project is intended for educational, portfolio, and demonstration purposes.

Add an appropriate license before distributing the project publicly.
