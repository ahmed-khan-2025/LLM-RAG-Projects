# LLM-RAG-Projects

A collection of practical **Large Language Model (LLM)** and **Retrieval-Augmented Generation (RAG)** projects built with Python.

This repository demonstrates the development of AI applications using **RAG pipelines, LLMs, APIs, audio processing, and multimodal data**.

---

## 🚀 Projects

### 🤖 LLM RAG API

**Folder:** `llm-rag-api`

A FastAPI-based RAG application that provides an API interface for querying documents using Large Language Models.

**Key concepts:**

- FastAPI
- RAG architecture
- Document ingestion
- Text chunking
- Embeddings
- Vector search
- LLM integration
- REST API
- Local and cloud LLMs

**LLM providers explored:**

- Ollama
- OpenAI
- Google Gemini

---
### 🎧 Audio RAG Assistant

**Folder:** `audio-rag-assistant`

An AI assistant that combines audio processing with Retrieval-Augmented Generation.

**Key concepts:**

- Audio processing
- Speech-to-text
- Document retrieval
- Semantic search
- LLM-based question answering
- RAG pipeline


---

### 🎥 Multimodal RAG Assistant

**Folder:** `multimodal-rag-assistant`

A multimodal RAG application exploring how AI systems can retrieve and generate information from different types of content.

**Key concepts:**

- Multimodal AI
- RAG
- LLMs
- Text processing
- Audio processing
- Image/video understanding
- Embeddings
- Semantic retrieval

---

## 🏗️ RAG Architecture

The general architecture used across these projects is:

```text
                    User
                      │
                      ▼
              ┌───────────────┐
              │   FastAPI /   │
              │  Application  │
              └───────┬───────┘
                      │
                      ▼
              ┌───────────────┐
              │  RAG Pipeline │
              ├───────────────┤
              │ Document Load │
              │ Chunking      │
              │ Embeddings    │
              │ Retrieval     │
              └───────┬───────┘
                      │
                      ▼
              ┌───────────────┐
              │ Vector Search │
              └───────┬───────┘
                      │
                      ▼
              ┌───────────────┐
              │      LLM      │
              │ Ollama/OpenAI │
              │    Gemini     │
              └───────┬───────┘
                      │
                      ▼
              ┌───────────────┐
              │ Final Answer  │
              └───────────────┘