# Simple LLM RAG Application

A simple Retrieval-Augmented Generation (RAG) application built with Python, FastAPI, Sentence Transformers, NumPy, and Ollama.

## Architecture

```text
                 Employee Handbook
                        |
                        v
                  Text Chunks
                        |
                        v
                  Embeddings
                        |
                        v
                 Similarity Search
                        |
User Question ---------+
                        |
                        v
                 Relevant Context
                        |
                        v
                      Ollama
                        |
                        v
                     Answer
```

## Technologies

* Python
* FastAPI
* Ollama
* Sentence Transformers
* NumPy
* Pytest
* Docker
* GitHub Actions

## Features

* Load a text document
* Split document into chunks
* Generate embeddings
* Search for relevant document chunks
* Send relevant context to an LLM
* Generate an answer
* Return source chunks
* REST API
* Swagger/OpenAPI documentation
* Automated tests
* Docker support
* GitHub Actions CI

## Installation

Create a virtual environment:

```powershell
py -3.10 -m venv .venv
```

Activate it:

```powershell
.venv\Scripts\activate
```

Install dependencies:

```powershell
python -m pip install -r requirements.txt
```

## Ollama

Install Ollama and download the model:

```powershell
ollama pull llama3.2
```

Test Ollama:

```powershell
ollama run llama3.2
```

## Run the API

```powershell
python -m uvicorn app.main:app --reload
```

Open Swagger:

```text
http://127.0.0.1:8000/docs
```

## Example Request

```json
{
    "question": "How many vacation days do employees receive?"
}
```

## Example Response

```json
{
    "question": "How many vacation days do employees receive?",
    "answer": "Full-time employees receive 25 vacation days per calendar year.",
    "sources": [
        {
            "text": "...",
            "score": 0.75
        }
    ]
}
```

## Run Tests

```powershell
python -m pytest -v
```

## Docker

Build and run:

```powershell
docker compose up --build
```

Then open:

```text
http://localhost:8000/docs
```

## CI/CD

GitHub Actions automatically:

1. Checks out the repository
2. Installs Python 3.10
3. Installs dependencies
4. Runs pytest

## Project Purpose

This project demonstrates the basic architecture of a Retrieval-Augmented Generation system and provides a foundation for adding document upload, vector databases, authentication, monitoring, and production deployment.
