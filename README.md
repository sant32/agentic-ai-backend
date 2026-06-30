# Agentic RAG Backend

A production-oriented **Agentic Retrieval-Augmented Generation (RAG)** backend built with **FastAPI**, **LangGraph**, **Qdrant**, and **PostgreSQL**. The project focuses on scalable document ingestion, hybrid retrieval, secure authentication, and an extensible architecture for AI agents.

> **Status:** 🚧 Active Development

---

# Features

## Authentication

- JWT Authentication
- Access Token
- Refresh Token Rotation
- User Registration
- Login
- Protected Endpoints
- User-specific document isolation

---

## Document Ingestion

- PDF document ingestion
- Metadata extraction
- Recursive text chunking
- User metadata attachment
- Chunk metadata generation
- Batch embedding generation

---

## Embeddings

### Dense Embeddings

- Mistral Embedding Model
- Async batch processing
- Semaphore-based concurrency control

### Sparse Embeddings

- Sparse embedding generation
- Hybrid search support

---

## Vector Database

- Qdrant Vector Database
- Collection management
- Dense vector storage
- Sparse vector storage
- Payload metadata storage
- Batch upserts

---

## Hybrid Search

- Dense + Sparse retrieval
- Reciprocal Rank Fusion (RRF)
- Metadata filtering
- User-level document isolation
- Configurable Top-K retrieval

---

## Architecture

- Service-oriented architecture
- Dependency injection
- Async-first implementation
- Modular components
- Separation of concerns

---

# Tech Stack

| Category | Technology |
|----------|------------|
| Backend | FastAPI |
| AI Framework | LangChain |
| Agent Framework | LangGraph *(Upcoming)* |
| LLM | Mistral |
| Embeddings | Mistral Embeddings |
| LLM Gateway | LiteLLM |
| Vector Database | Qdrant |
| Database | PostgreSQL (Neon) |
| Authentication | JWT |
| Language | Python 3.11+ |

---

# Current Project Structure

```text
app/
│
├── api/
│
├── auth/
│
├── core/
│
├── services/
│   ├── chunking_service.py
│   ├── embedding_service.py
│   ├── sparse_embedding_service.py
│   ├── vector_service.py
│   ├── ingestion_service.py
│   ├── search_service.py
│   └── llm_service.py
│
├── guardrails/
│   ├── pii_masking_service.py
│   └── prompt_injection_service.py
│
├── graph/
│   ├── nodes.py
│   ├── edges.py
│   └── state.py
│
└── models/
```

---

# Retrieval Pipeline

```text
User Query
      │
      ▼
Dense Embedding
      │
      ▼
Sparse Embedding
      │
      ▼
Metadata Filter
      │
      ▼
Hybrid Search (Qdrant)
      │
      ▼
Retrieved Documents
```

---

# Document Ingestion Pipeline

```text
PDF
 │
 ▼
Chunking
 │
 ▼
Dense Embedding
 │
 ▼
Sparse Embedding
 │
 ▼
Vector Store (Qdrant)
```

---

# Metadata Stored

Each chunk contains metadata similar to:

```json
{
  "user_id": 11,
  "document_id": "AI_Guide_ab12cd34",
  "chunk_id": "AI_Guide_chunk_12",
  "page": 5,
  "source": "AI_Guide.pdf"
}
```

---

# Implemented

- [x] JWT Authentication
- [x] Access Token
- [x] Refresh Token Rotation
- [x] User Authentication
- [x] PDF Ingestion
- [x] Recursive Chunking
- [x] Dense Embeddings
- [x] Sparse Embeddings
- [x] Batch Embedding
- [x] Vector Storage
- [x] Hybrid Search
- [x] Metadata Filtering
- [x] User-level Isolation
- [x] Dependency Injection
- [x] Async Service Architecture

---

# Upcoming Features

## LangGraph Integration

- [ ] Graph-based workflow orchestration
- [ ] State management
- [ ] Retrieval node
- [ ] Generation node
- [ ] Conditional routing
- [ ] Multi-step reasoning

---

## Guardrails

- [ ] Prompt Injection Detection
- [ ] PII Masking
- [ ] Output Validation

---

## Retrieval

- [ ] Cross Encoder Re-ranking
- [ ] Query Rewriting
- [ ] Multi-query Retrieval
- [ ] Context Compression

---

## LLM

- [ ] LiteLLM Gateway Integration
- [ ] Automatic Model Fallback
- [ ] Streaming Responses
- [ ] Token Usage Tracking

---

## Memory

- [ ] Conversation Memory
- [ ] Session Memory
- [ ] Persistent Chat History

---

## Evaluation & Observability

- [ ] RAGAS Evaluation
- [ ] LangSmith Tracing
- [ ] OpenTelemetry
- [ ] Performance Metrics

---

## Background Processing

- [ ] Async Ingestion Queue
- [ ] Background Embedding Generation
- [ ] Retry Mechanism

---

# Future Architecture

```text
                User Query
                     │
                     ▼
          Prompt Injection Check
                     │
                     ▼
               PII Masking
                     │
                     ▼
             Query Rewriting
                     │
                     ▼
              Hybrid Retrieval
                     │
                     ▼
               Re-ranking
                     │
                     ▼
            LangGraph Workflow
                     │
        ┌────────────┴────────────┐
        ▼                         ▼
 Retrieval Node            Tool Calling
        │                         │
        └────────────┬────────────┘
                     ▼
               Prompt Builder
                     │
                     ▼
          LiteLLM Gateway (Fallback)
                     │
                     ▼
               Mistral LLM
                     │
                     ▼
                 Final Answer
```

---

# Goals

- Production-ready architecture
- Scalable service design
- Modular codebase
- Hybrid semantic retrieval
- Secure authentication
- Agentic workflow support
- Enterprise-ready RAG pipeline