# AI Generation & Evaluation Platform

A production-oriented **LLMOps / RAG platform** designed to demonstrate the engineering around foundation models rather than model training.

The project focuses on the production lifecycle of AI generation:

* Prompt and system-instruction versioning
* Brand environments and brand-specific rules
* Brand-aware RAG
* PostgreSQL + pgvector
* Model/provider routing abstraction
* Local foundation-model inference with Ollama
* Safety and off-brand guardrails
* Automated quality evaluation
* Groundedness evaluation
* Input/output token tracking
* Estimated generation cost tracking
* Latency and failure monitoring
* Prometheus metrics
* Grafana observability
* PostgreSQL generation-event logging
* Dockerized infrastructure
* Automated tests with pytest

---

# Technology Stack

| Area              | Technology              |
| ----------------- | ----------------------- |
| Language          | Python 3.10             |
| API               | FastAPI                 |
| Database          | PostgreSQL              |
| Vector Search     | pgvector                |
| LLM Runtime       | Ollama                  |
| Embeddings        | Sentence Transformers   |
| Data Processing   | Python                  |
| Monitoring        | Prometheus              |
| Visualization     | Grafana                 |
| Containers        | Docker / Docker Compose |
| Testing           | pytest                  |
| API Documentation | Swagger / OpenAPI       |

---

# Windows Setup

## 1. Open the project

```powershell
cd "C:\Galib\ABC-Personal\4 Own Python Projects\RAG Project\ai-generation-evaluation-platform"
```

If your project is located somewhere else, replace the path with your actual project path.

---

## 2. Create Python 3.10 environment

Create the virtual environment:

```powershell
py -3.10 -m venv .venv
```

Activate it:

```powershell
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

Verify Python:

```powershell
python --version
```

Expected:

```text
Python 3.10.x
```

---

# 3. Install Python dependencies

Upgrade pip:

```powershell
python -m pip install --upgrade pip
```

Install project dependencies:

```powershell
pip install -r requirements.txt
```

---

# 4. Configure environment variables

Create the environment file:

```powershell
copy .env.example .env
```

Update `.env` according to your local configuration.

The project is designed to use **Ollama for local LLM inference**, so an OpenAI API key is not required for the current implementation.

---

# 5. Start infrastructure

Start PostgreSQL, Prometheus and Grafana:

```powershell
docker compose up -d
```

Check running containers:

```powershell
docker ps
```

Current project infrastructure:

```text
PostgreSQL   → localhost:5436
Prometheus   → localhost:9091
Grafana      → localhost:3002
FastAPI      → localhost:8003
```

The FastAPI application currently runs directly from the Python environment, while PostgreSQL, Prometheus and Grafana run in Docker.

---

# 6. Verify PostgreSQL

The project PostgreSQL container is:

```text
ai-generation-postgres
```

Host port:

```text
5436
```

The application connects to PostgreSQL using the configuration defined in `.env`.

---

# 7. Start Ollama

Check installed models:

```powershell
ollama list
```

If `llama3.2:latest` is not available:

```powershell
ollama pull llama3.2
```

Check Ollama:

```text
http://localhost:11434
```

Ollama provides the local foundation-model inference layer.

---

# 8. Start FastAPI

Start the application:

```powershell
uvicorn app.main:app --host 0.0.0.0 --port 8003 --reload
```

The API will be available at:

```text
http://127.0.0.1:8003
```

Swagger / OpenAPI:

```text
http://127.0.0.1:8003/docs
```

Metrics:

```text
http://127.0.0.1:8003/metrics
```

---

# 9. Prometheus

Prometheus runs in Docker and is exposed on:

```text
http://127.0.0.1:9091
```

The Prometheus container uses its internal port `9090`.

---

# 10. Verify Prometheus Target

Open:

```text
http://127.0.0.1:9091/targets
```

---

# 11. Grafana

Grafana runs in Docker and is available at:

```text
http://127.0.0.1:3002
```

---

# First API Workflow

## Step 1 — Create a Brand

Endpoint:

```text
POST /brands
```

---

# Step 2 — Create a Prompt Version

Endpoint:

```text
POST /prompts
```
---

# Step 3 — Upload Brand Knowledge

Endpoint:

```text
POST /documents/upload
```

Use:

```text
brand_name=DemoFashion
```

Upload a `.txt`, `.pdf` or `.docx` document containing brand or product information.

---

# Step 4 — Generate Content

Endpoint:

```text
POST /generate
```

---

# Evaluation

Endpoint:

```text
POST /evaluate
```

The evaluation layer provides deterministic first-line checks for:

* Quality
* Groundedness
* Safety
* Brand compliance

---

# Observability

The application exposes Prometheus metrics through:

```text
/metrics
```

---

# Grafana Monitoring

The monitoring architecture is:

```text
FastAPI
   |
   | /metrics
   v
Prometheus
   |
   v
Grafana
```

Example Prometheus queries:

### API availability

```promql
up{instance="host.docker.internal:8003"}
```


### Total generations

```promql
ai_generation_total
```

### Generation failures

```promql
ai_generation_failures_total
```

### Active requests

```promql
ai_generation_active_requests
```

### Generation latency

```promql
ai_generation_latency_seconds
```

These metrics provide the foundation for an operational AI/LLM monitoring dashboard.

---

# RAG Pipeline

The RAG implementation uses PostgreSQL with pgvector.

```text
Brand Document
      |
      v
Text Extraction
      |
      v
Chunking
      |
      v
Embedding Model
      |
      v
Vector
      |
      v
PostgreSQL + pgvector
      |
      v
Similarity Search
      |
      v
Top-K Brand Context
      |
      v
LLM Prompt
      |
      v
Generated Response
```

Retrieval is scoped by brand so that one brand's information is not accidentally used for another brand.

---

# Testing

Run the complete test suite:

```powershell
python -m pytest -v
```

---

# Production Engineering Concepts Demonstrated

This project demonstrates several concepts relevant to an **AI Platform Engineer / ML Engineer / LLMOps Engineer** role.

### Prompt Operations

Prompt versions are persisted and can be activated independently from application deployments.

### Brand Environments

Each brand has its own:

* Tone
* Required terms
* Forbidden terms
* Safety rules
* Knowledge base

### Retrieval

Documents are embedded and stored in pgvector, enabling semantic retrieval of brand-specific information.

### Model Abstraction

The model provider is isolated behind a routing layer, allowing future provider integrations.

### Evaluation

Generation quality and groundedness are evaluated automatically.

### Guardrails

Generated content is checked against safety and brand-specific rules.

### Cost Tracking

Input/output token usage can be used to estimate generation cost.

### Observability

Prometheus and Grafana provide operational monitoring for AI generation.

### Event Logging

Generation events and metadata are persisted in PostgreSQL for analysis and auditing.

---

# Future Production Upgrades

Possible next improvements include:

1. Add OpenAI provider adapter.
2. Add Anthropic provider adapter.
3. Implement policy-based model routing.
4. Add model fallback and retry strategies.
5. Add prompt A/B testing.
6. Add LLM-as-a-judge evaluation.
7. Add a golden evaluation dataset.
8. Add RAG Recall@K.
9. Add MRR and nDCG retrieval evaluation.
10. Add semantic caching with Redis.
11. Add PII/GDPR detection and redaction.
12. Add image-generation provider adapters.
13. Add video-generation provider adapters.
14. Add human approval workflows.
15. Add CI/CD pipelines.
16. Deploy to Kubernetes.
17. Add OpenTelemetry distributed tracing.
18. Integrate an LLM observability platform such as Langfuse.
19. Add model-quality regression testing.
20. Add automated evaluation gates before production rollout.

## Key Engineering Areas

```text
Python
FastAPI
LLMOps
RAG
PostgreSQL
pgvector
Ollama
Prompt Engineering
Model Routing
Evaluation
Guardrails
Observability
Prometheus
Grafana
Docker
pytest
```

---

# Summary

This project demonstrates the engineering layer around foundation models:

```text
Prompt Management
       +
Brand Configuration
       +
RAG / Retrieval
       +
Model Routing
       +
LLM Inference
       +
Safety
       +
Evaluation
       +
Cost Tracking
       +
Observability
       +
Event Logging
       =
AI Generation Platform
```

The focus is not on training a foundation model.

The focus is on **how an AI platform operates, evaluates, monitors and controls foundation-model generation in a production-oriented environment.**
