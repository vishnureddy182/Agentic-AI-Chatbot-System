# AI Chatbot System

An enterprise-grade AI chatbot for eCommerce, combining **Retrieval-Augmented Generation (RAG)** with a **multi-agent architecture** to answer product questions, manage orders, and escalate issues to a human when needed.

---

## What this is

- A RAG pipeline that answers questions grounded in your own documents, with source citations
- A LangGraph-based multi-agent system that routes requests to specialist agents (RAG, orders, products, escalation, voice)
- Pluggable LLM backends (OpenAI, Anthropic Claude, local Ollama) with automatic fallback
- Production concerns built in from day one: auth, rate limiting, observability, and a full test suite

**145 files across 16 functional areas**, built in 3 delivery phases over 20 weeks.

---

## Tech stack

| Layer | Technology |
|---|---|
| API | FastAPI |
| LLMs | OpenAI GPT-4o, Anthropic Claude 3.5 Sonnet, local Llama 3 via Ollama |
| Orchestration | LangChain, LangGraph |
| Vector store | ChromaDB (dev), Qdrant (prod) |
| Database | PostgreSQL, Redis (cache) |
| Frontend | Python (Streamlit/Gradio-style) |
| Infra | Docker Compose, Terraform, Kubernetes |
| Observability | Prometheus, Grafana, LangSmith |

---

## Folder structure

```
AI_Chatbot_System/
├── app.py                    # FastAPI app factory, router registration
├── config.py                 # Pydantic Settings — all env vars & feature flags
├── utils.py                  # Shared helpers: chunking, sanitisation, hashing
├── requirements.txt
├── docker-compose.yml        # Orchestrates API + Redis + Qdrant + Postgres + Grafana
├── Dockerfile
│
├── models/                   # Pluggable LLM providers (OpenAI, Claude, Ollama, fine-tuned)
├── rag/                      # Ingest → chunk → embed → store → retrieve → cite
├── agents/                   # LangGraph multi-agent orchestration + supervisor
├── tools/                    # Agent-callable functions (orders, products, cart, payments...)
├── integrations/             # Third-party API clients (Shopify, Stripe, Twilio, Deepgram...)
├── security/                 # Auth, RBAC, input validation, prompt-injection guard, rate limiting
├── database/                 # CRUD operations, ORM models, Redis cache, migrations
├── routers/                  # FastAPI endpoints (chat, auth, documents, admin, voice...)
├── prompts/                  # Version-controlled prompt templates
├── observability/            # Logging, health checks, metrics, tracing, Grafana dashboards
├── tests/                    # Unit, integration, RAG-eval, load, and security test suites
├── frontend/                 # Python-based UI (chat widget, admin panel, dashboards)
├── fine_tuning/              # LoRA/QLoRA pipeline for a custom domain model
├── infra/                    # Terraform + Kubernetes infrastructure-as-code
├── .github/workflows/        # CI/CD pipelines (test, deploy, security scan)
└── docs/                     # API reference and architecture diagram
```

For the full file-by-file tree with phase tags, see [`docs/api_reference.md`](docs/api_reference.md) or the project's folder-structure report.

---

## Getting started

### Prerequisites

- Docker and Docker Compose
- Python 3.11+
- API keys for at least one LLM provider (OpenAI and/or Anthropic), or Ollama running locally for a zero-cost setup

### Setup

```bash
# 1. Clone and enter the project
cd AI_Chatbot_System

# 2. Copy the environment template and fill in your keys
cp .env.example .env

# 3. Start the full stack (API + Redis + Qdrant + Postgres + Grafana)
docker compose up

# 4. Confirm the API is healthy
curl http://localhost:8000/health
```

### Install dependencies locally (without Docker)

```bash
pip install -r requirements.txt
uvicorn app:app --reload
```

### Run the test suite

```bash
pytest
```

---

## How a request flows through the system

```
User → security/ (auth, rate-limit, prompt guard)
     → routers/ (chat.py routes the request)
     → agents/ (supervisor picks the right specialist agent)
     → rag/ + tools/ (retrieve context or call a business tool)
     → models/ (the LLM generates the answer)
     → response, with citations where relevant
```

Supporting layers wrap every request: `database/` stores history and cache, `observability/` logs and traces each step, `integrations/` talks to external services, and `prompts/` supplies the templates used at each stage.

---

## Build roadmap

The project is built in three phases, with every file tagged `[MVP]`, `[P2]`, or `[P3]` to make scope explicit.

### Phase 1 — MVP (Weeks 1–6): Core Chat + RAG
A working chatbot that answers from your own documents, behind basic auth.

| Week | Focus |
|---|---|
| 1 | Scaffold the repo — Docker Compose, FastAPI boot, config |
| 2 | Wire up one LLM provider end-to-end, then the other two |
| 3 | Build RAG ingestion — load, chunk, embed, store |
| 4 | Build RAG retrieval — query, retrieve, cite sources |
| 5 | Add auth/RBAC/input validation, expose core routers |
| 6 | Core test suite + a minimal chat UI |

### Phase 2 — Agents + Business Tools (Weeks 7–12)
The chatbot can take real actions, not just answer questions.

| Week | Focus |
|---|---|
| 7 | Define the LangGraph state machine and supervisor |
| 8 | Build the real specialist agents |
| 9 | Give agents real tools (orders, products, cart) |
| 10 | Connect a real eCommerce backend (Shopify/WooCommerce) |
| 11 | Harden security, add Redis caching |
| 12 | Add metrics, tracing, dashboards, and RAG-quality evaluation |

### Phase 3 — Voice, Scale & Fine-Tuning (Weeks 13–20)
Production-scale, multi-channel, and a custom fine-tuned model.

| Weeks | Focus |
|---|---|
| 13–14 | Payment integrations (Stripe/Razorpay) |
| 15 | Speech-to-text / text-to-speech + voice agent |
| 16 | Voice endpoint + minimal voice UI |
| 17 | SMS/Slack/Teams notifications + webhooks |
| 18 | Move to real cloud infra (Terraform/Kubernetes), automate deployment |
| 19 | Load testing + OWASP/prompt-injection security testing |
| 20 | Fine-tune and publish a custom LoRA adapter |

---

## Project status

🚧 In active development — currently in **Phase 1 (MVP)**.

---

## License

Internal project — license to be determined.
