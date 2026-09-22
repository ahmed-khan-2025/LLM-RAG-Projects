# Multimodal RAG Assistant

A **Multimodal Retrieval-Augmented Generation (RAG) Assistant** that can understand and retrieve information from both **video audio and visual content**.

The system processes a video by extracting:

* 🎙️ Audio → speech transcription with timestamps
* 🎞️ Video frames → visual descriptions using a vision-capable LLM
* 🧩 Text → semantic chunks
* 🔎 Embeddings → vector representations
* 🗂️ ChromaDB → vector storage
* 🔤 BM25 → keyword-based retrieval
* 🎯 Cross-Encoder → result reranking
* 🤖 Ollama → local LLM generation

The final answer is generated from retrieved evidence and can include **video timestamps** showing where the information was found.

---

## 🚀 Key Features

* 🎥 Video ingestion
* 🎙️ Automatic audio extraction
* 🗣️ Speech-to-text using Faster-Whisper
* ⏱️ Timestamped transcription
* 🖼️ Automatic video-frame extraction
* 👁️ Visual understanding using a vision LLM
* 🧩 Audio and visual document chunking
* 🧠 Sentence-transformer embeddings
* 🗃️ ChromaDB vector database
* 🔤 BM25 keyword search
* 🔀 Hybrid retrieval
* 🎯 Cross-Encoder reranking
* 🤖 Local LLM inference using Ollama
* 📚 Grounded RAG responses
* ⏱️ Timestamp-based evidence
* ⚡ FastAPI REST API
* 📖 Swagger/OpenAPI documentation
* 🧪 Pytest test suite
* 🐳 Docker-ready architecture
* 🔌 Provider-independent LLM interface

---

# 🏗️ Architecture

```text
                         VIDEO
                           │
             ┌─────────────┴─────────────┐
             │                           │
             ▼                           ▼
          AUDIO                        FRAMES
             │                           │
             ▼                           ▼
       Faster-Whisper               Vision LLM
             │                           │
             ▼                           ▼
      Transcript + Time          Visual Descriptions
             │                           │
             └─────────────┬─────────────┘
                           │
                           ▼
                  Multimodal Chunks
                           │
                 ┌─────────┴─────────┐
                 │                   │
                 ▼                   ▼
             ChromaDB               BM25
          Vector Search         Keyword Search
                 │                   │
                 └─────────┬─────────┘
                           │
                           ▼
                    Hybrid Retrieval
                           │
                           ▼
                    Cross-Encoder
                      Reranking
                           │
                           ▼
                     Context Fusion
                           │
                           ▼
                      Ollama LLM
                           │
                           ▼
                 Grounded Answer
                           │
                           ▼
              Timestamps / Evidence
```

---

# 📁 Project Structure

```text
multimodal-rag-assistant/
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
│   ├── video/
│   │   ├── __init__.py
│   │   ├── extractor.py
│   │   ├── frame_sampler.py
│   │   └── vision.py
│   │
│   ├── rag/
│   │   ├── __init__.py
│   │   ├── models.py
│   │   ├── chunker.py
│   │   ├── embeddings.py
│   │   ├── vector_store.py
│   │   ├── hybrid_search.py
│   │   ├── reranker.py
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
│   ├── videos/
│   ├── audio/
│   ├── frames/
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

# 🧰 Technology Stack

| Component         | Technology            |
| ----------------- | --------------------- |
| API               | FastAPI               |
| Language          | Python                |
| Speech-to-Text    | Faster-Whisper        |
| Video Processing  | OpenCV                |
| Embeddings        | Sentence Transformers |
| Vector Database   | ChromaDB              |
| Keyword Search    | BM25                  |
| Reranking         | Cross-Encoder         |
| LLM               | Ollama                |
| Vision Model      | Llama Vision          |
| API Documentation | Swagger / OpenAPI     |
| Testing           | Pytest                |
| Containerization  | Docker                |

---

# 🔄 How the System Works

## 1. Upload Video

The user uploads a video through the FastAPI endpoint.

```text
POST /video/upload
```

Example:

```text
training.mp4
```

---

## 2. Extract Audio

The audio track is extracted from the video.

```text
training.mp4
      │
      ▼
training.wav
```

The audio is then passed to Faster-Whisper.

---

## 3. Speech Transcription

Faster-Whisper converts speech into text.

Example:

```text
00:00 - 00:08
"Welcome to the employee safety training."

00:08 - 00:17
"All employees must complete the safety course."

00:17 - 00:25
"The training must be completed within 30 days."
```

The timestamps are preserved.

---

# 4. Extract Video Frames

The system samples frames from the video.

For example:

```text
00:00 → Frame 1
00:10 → Frame 2
00:20 → Frame 3
00:30 → Frame 4
...
```

The sampling interval can be configured using:

```env
FRAME_INTERVAL=10
```

---

# 5. Visual Understanding

The extracted frames are sent to a vision-capable LLM.

Example:

```text
Frame timestamp: 00:20

Visual description:

"A presenter is standing in front of a
large screen displaying a workplace
safety checklist."
```

The visual description becomes searchable text.

---

# 6. Create Multimodal Chunks

Audio and visual information are converted into structured chunks.

Example audio chunk:

```text
Type: audio

Start: 00:08
End: 00:17

Text:
"All employees must complete the safety course."
```

Example visual chunk:

```text
Type: visual

Timestamp: 00:20

Description:
"A presenter is displaying a workplace
safety checklist."
```

---

# 7. Generate Embeddings

The textual content is converted into vectors using a sentence-transformer model.

Example:

```text
"employee safety training"
              │
              ▼
       Embedding Model
              │
              ▼
     [0.21, -0.14, 0.72, ...]
```

These vectors are stored in ChromaDB.

---

# 8. Hybrid Retrieval

The system uses two retrieval strategies.

### Semantic Search

ChromaDB finds content based on semantic similarity.

```text
User question
      │
      ▼
Query Embedding
      │
      ▼
ChromaDB
      │
      ▼
Relevant chunks
```

### Keyword Search

BM25 finds exact or closely matching terms.

```text
User question
      │
      ▼
BM25
      │
      ▼
Keyword matches
```

The results are combined.

```text
Vector Search
      +
BM25 Search
      │
      ▼
Hybrid Results
```

---

# 9. Reranking

The retrieved results are passed to a Cross-Encoder reranker.

```text
Retrieved Results
       │
       ▼
Cross-Encoder
       │
       ▼
Ranked Results
       │
       ▼
Top Relevant Chunks
```

This helps improve retrieval precision before sending context to the LLM.

---

# 10. RAG Generation

The retrieved information is inserted into a prompt.

Example:

```text
Context:

[00:08 - 00:17]
All employees must complete the safety course.

[00:20]
A workplace safety checklist is displayed.

Question:

When must employees complete the safety course?
```

The LLM generates an answer using the retrieved context.

---

# 🤖 LLM Provider Architecture

The application uses an abstraction layer for LLM providers.

```text
                  LLMInterface
                       │
          ┌────────────┼────────────┐
          │            │            │
       Ollama        OpenAI       Gemini
```

This means the RAG system is not tightly coupled to one LLM provider.

The provider can be changed through configuration.

---

# 🦙 Ollama

This project is designed to support local LLM inference through Ollama.

Start Ollama and verify that it is running:

```bash
ollama list
```

Pull the required models:

```bash
ollama pull llama3.2
```

For visual analysis, use a vision-capable model supported by your Ollama installation, for example:

```bash
ollama pull llama3.2-vision:11b
```

---

# 🐍 Python Environment

Python **3.10 or 3.11** is recommended for this project because several machine-learning and audio/video packages can have compatibility issues with newer Python versions.

Create a virtual environment:

```bash
python -m venv .venv
```

Activate on Windows:

```bash
.venv\Scripts\activate
```

Verify:

```bash
python --version
```

---

# 📦 Installation

Install the dependencies:

```bash
pip install -r requirements.txt
```

Example `requirements.txt`:

```text
fastapi
uvicorn[standard]
python-multipart
python-dotenv
faster-whisper
opencv-python
sentence-transformers
chromadb
rank-bm25
numpy
requests
pydantic
pytest
httpx
```

---

# 🎬 FFmpeg

FFmpeg is required for extracting audio from video files.

Verify installation:

```bash
ffmpeg -version
```

If the command is not recognized, install FFmpeg and make sure it is available in the system PATH.

---

# ⚙️ Environment Configuration

Create a `.env` file:

```env
LLM_PROVIDER=ollama

OLLAMA_URL=http://localhost:11434
OLLAMA_MODEL=llama3.2

VISION_MODEL=llama3.2-vision:11b

WHISPER_MODEL=base
WHISPER_DEVICE=cpu
WHISPER_COMPUTE_TYPE=int8

EMBEDDING_MODEL=all-MiniLM-L6-v2

RERANKER_MODEL=cross-encoder/ms-marco-MiniLM-L-6-v2

CHROMA_PATH=data/chroma
CHROMA_COLLECTION=multimodal_documents

BM25_PATH=data/bm25_index.json

VIDEO_PATH=data/videos
AUDIO_PATH=data/audio
FRAME_PATH=data/frames

FRAME_INTERVAL=10

TOP_K_VECTOR=8
TOP_K_BM25=8
TOP_K_RERANK=5

CHUNK_SIZE=500
CHUNK_OVERLAP=100

MAX_CONTEXT_CHARS=12000
```

---

# ▶️ Run the Application

Start FastAPI:

```bash
uvicorn app.main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

Swagger documentation:

```text
http://127.0.0.1:8000/docs
```

---

# 🔌 API Endpoints

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

# 🎥 Upload Video

```http
POST /video/upload
```

The endpoint:

1. Saves the video
2. Extracts audio
3. Transcribes audio
4. Extracts video frames
5. Generates visual descriptions
6. Creates chunks
7. Generates embeddings
8. Stores the content
9. Makes the video searchable

---

# 💬 Ask a Question

```http
POST /chat
```

Example request:

```json
{
  "question": "What does the presenter say about employee safety training?"
}
```

Example response:

```json
{
  "question": "What does the presenter say about employee safety training?",
  "answer": "The presenter explains that all employees must complete the safety training within 30 days.",
  "sources": [
    {
      "type": "audio",
      "start": 8.0,
      "end": 17.0,
      "text": "All employees must complete the safety course."
    },
    {
      "type": "visual",
      "timestamp": 20.0,
      "text": "A workplace safety checklist is displayed."
    }
  ]
}
```

---

# ⏱️ Timestamp-Based Answers

One important feature of this project is that retrieved information maintains its original video location.

For example:

```text
Answer:
Employees must complete the safety course within 30 days.

Evidence:
00:08 - 00:17
```

This allows a user to go directly to the relevant part of the video.

---

# 🧠 Why Multimodal RAG?

Traditional text RAG mainly works with:

```text
Documents
   ↓
Text
   ↓
Embeddings
   ↓
Vector Search
   ↓
LLM
```

A video contains much more information:

```text
                  VIDEO
                    │
        ┌───────────┴───────────┐
        │                       │
       Audio                  Visual
        │                       │
    Transcript                Frames
        │                       │
        └───────────┬───────────┘
                    │
              Multimodal RAG
                    │
                    ▼
                   LLM
```

This allows the system to answer questions about both **what was said** and **what was shown**.

---

# 🔎 Example Questions

The assistant can answer questions such as:

### Audio-based

```text
What did the presenter say about safety training?
```

### Visual-based

```text
What is displayed on the screen around 2 minutes into the video?
```

### Combined

```text
What safety procedure does the presenter explain,
and what is shown on the screen while explaining it?
```

### Timestamp-based

```text
When does the presenter start discussing emergency procedures?
```

### Semantic search

```text
What does the video say about employee responsibilities?
```

---

# 🧪 Testing

Run all tests:

```bash
python -m pytest -v
```

Example:

```text
============================= test session starts =============================

tests/test_chunker.py::test_chunking PASSED
tests/test_api.py::test_health PASSED

============================== 2 passed =======================================
```

Using:

```bash
python -m pytest -v
```

is completely valid, especially when the `pytest` executable is not available directly in your PATH.

---

# 🐳 Docker

Build the Docker image:

```bash
docker build -t multimodal-rag-assistant .
```

Run:

```bash
docker run -p 8000:8000 multimodal-rag-assistant
```

For production deployments, external services such as GPU-based inference, persistent vector storage, and object storage can be added.

---

# 🔐 Security Considerations

For production deployment, consider adding:

* Authentication
* Authorization
* API keys
* File-size limits
* Allowed video formats
* MIME-type validation
* Upload quotas
* Rate limiting
* Input validation
* Secure temporary file handling
* Prompt-injection protection
* Logging and monitoring
* Secure model configuration

---

# 📈 Current Architecture vs. Advanced Architecture

The current system already includes several advanced RAG components:

```text
Video
 ↓
Audio + Frames
 ↓
Whisper + Vision Model
 ↓
Chunking
 ↓
Embeddings
 ↓
Vector Search + BM25
 ↓
Hybrid Retrieval
 ↓
Cross-Encoder Reranking
 ↓
Context Fusion
 ↓
LLM
 ↓
Answer + Evidence
```

This goes significantly beyond a basic:

```text
PDF → Embeddings → Vector DB → LLM
```

The visual information is currently converted into **text descriptions** before embedding and retrieval. A future version can perform true cross-modal retrieval using native image/video embeddings.

---

# 🚀 Future Improvements

## 1. Speaker Diarization

Identify different speakers:

```text
Speaker 1:
"We need to improve production quality."

Speaker 2:
"The new process will start next month."
```

---

## 2. Better Frame Sampling

Instead of extracting frames every fixed number of seconds, detect important visual changes.

```text
Scene Change Detection
        ↓
Important Frames
        ↓
Vision Analysis
```

---

## 3. True Multimodal Embeddings

Instead of converting every frame into text first:

```text
Image
  ↓
Image Embedding
```

and:

```text
Text
  ↓
Text Embedding
```

can be combined in a cross-modal retrieval system.

---

## 4. Conversation Memory

Support follow-up questions:

```text
User:
What is the main safety procedure?

Assistant:
The main procedure is...

User:
When does the presenter explain it?

Assistant:
It is explained around 03:20.
```

---

## 5. Multiple Videos

Allow the user to upload an entire video library:

```text
videos/
├── safety_training.mp4
├── onboarding.mp4
├── production_training.mp4
└── quality_control.mp4
```

Then ask:

```text
Which video discusses quality control?
```

---

## 6. Metadata Filtering

Support filtering by:

```text
video_id
speaker
timestamp
department
topic
date
```

---

## 7. Background Processing

For large videos:

```text
Upload
   ↓
Background Job
   ↓
Audio Processing
   ↓
Frame Processing
   ↓
Embedding
   ↓
Indexing
```

The API can immediately return a processing ID.

---

## 8. Production Infrastructure

Possible future architecture:

```text
                 API Gateway
                      │
                  FastAPI
                      │
             Background Workers
                      │
        ┌─────────────┼─────────────┐
        │             │             │
      Video         Whisper       Vision
    Processing      Service       Service
        │             │             │
        └─────────────┼─────────────┘
                      │
                Retrieval Layer
                      │
          ┌───────────┴───────────┐
          │                       │
       Vector DB                BM25
          │                       │
          └───────────┬───────────┘
                      │
                  Reranker
                      │
                    LLM
```

---

# 💼 Interview Explanation

A concise way to describe this project in an interview:

> I developed a multimodal RAG assistant that can process video content by combining speech transcription and visual information. Audio is transcribed with timestamps using Faster-Whisper, while sampled video frames are analyzed by a vision-capable LLM. The resulting information is chunked and indexed using semantic embeddings in ChromaDB and keyword retrieval with BM25. I then use hybrid retrieval and Cross-Encoder reranking before passing the most relevant context to a local Ollama LLM for grounded answer generation. The system also preserves timestamps so users can trace answers back to the original video.

---

# 🎯 Skills Demonstrated

This project demonstrates practical experience with:

* Python
* FastAPI
* REST API development
* RAG
* LLM applications
* Multimodal AI
* Speech-to-text
* Computer vision
* Video processing
* Prompt engineering
* Embeddings
* Vector databases
* Semantic search
* BM25
* Hybrid retrieval
* Reranking
* Local LLM inference
* Ollama
* ChromaDB
* Sentence Transformers
* Cross-Encoders
* Pytest
* Docker
* Modular software architecture

---

# 📌 Important Design Note

This project uses a **multimodal processing pipeline**, but the current retrieval layer primarily operates on text:

```text
Video
 ├── Audio → Transcript → Text Embedding
 │
 └── Frames → Vision Description → Text Embedding
```

Therefore, the system can retrieve information originating from both audio and visual content, while the actual vector search is performed over their textual representations.

A future fully multimodal implementation can use native image/video embeddings and cross-modal retrieval.

---

# 📄 License

This project is intended for educational, research, portfolio, and demonstration purposes.

Add an appropriate open-source license, such as MIT, if you intend to distribute the repository publicly.

---

# ⭐ Project Summary

**Multimodal RAG Assistant** combines:

```text
🎥 Video
   +
🎙️ Speech
   +
🖼️ Visual Understanding
   +
🧠 Embeddings
   +
🔎 Hybrid Search
   +
🎯 Reranking
   +
🤖 LLM
   =
🚀 Multimodal RAG Assistant
```

The project provides a practical foundation for building production-oriented AI systems capable of searching and answering questions about rich multimedia content.
