# University Bylaw RAG Chatbot

An AI-powered Retrieval-Augmented Generation (RAG) chatbot system for university bylaw and academic regulation documents.

The system allows students to ask natural language questions about university rules, academic regulations, examination procedures, attendance requirements, GPA calculations, course repeat policies, medical leave processes, and more.

Instead of manually searching through large PDF documents, students can receive accurate, contextual, and source-grounded answers instantly.

---

# Features

## Core Features

- AI-powered chatbot interface
- Semantic search over university bylaw documents
- PDF document ingestion and indexing
- Accurate contextual responses
- Source citations with page numbers
- Multi-document support
- Conversation memory
- Admin dashboard for document management
- Authentication system
- Chat history support

---

# Example Questions

```text
Can I repeat a failed course?

What happens if my attendance is below 80%?

What is the minimum GPA requirement for graduation?

Can I appeal examination results?

How many medical leaves are allowed?
```

---

# System Architecture

```text
                 ┌────────────────────┐
                 │     Next.js UI     │
                 │  Chat Interface    │
                 └─────────┬──────────┘
                           │ REST API
                           ▼
                 ┌────────────────────┐
                 │      FastAPI       │
                 │   RAG Backend      │
                 └─────────┬──────────┘
                           │
         ┌─────────────────┼──────────────────┐
         ▼                 ▼                  ▼
 ┌─────────────┐   ┌──────────────┐   ┌──────────────┐
 │ Vector DB   │   │ PostgreSQL   │   │ Object Store │
 │ pgvector    │   │ Chat Logs    │   │ PDFs          │
 └─────────────┘   └──────────────┘   └──────────────┘
                           │
                           ▼
                 ┌────────────────────┐
                 │ Embedding Models   │
                 │ + LLM Models       │
                 └────────────────────┘
```

---

# Tech Stack

# Frontend

| Technology | Purpose |
|---|---|
| Next.js | Frontend Framework |
| TypeScript | Type Safety |
| Tailwind CSS | Styling |
| shadcn/ui | UI Components |
| Zustand | State Management |
| Axios | API Communication |

---

# Backend

| Technology | Purpose |
|---|---|
| FastAPI | Backend API |
| Python 3.12+ | Main Language |
| SQLAlchemy | ORM |
| Pydantic | Data Validation |
| Uvicorn | ASGI Server |

---

# Database

| Technology | Purpose |
|---|---|
| PostgreSQL | Main Database |
| pgvector | Vector Storage |

---

# AI / RAG Stack

| Technology | Purpose |
|---|---|
| LangChain | RAG Orchestration |
| Sentence Transformers | Embedding Generation |
| Ollama | Local LLM Serving |
| HuggingFace Models | Open Source Models |

---

# Free Models (Initial Version)

## Embedding Model

```text
BAAI/bge-small-en-v1.5
```

Alternative:

```text
all-MiniLM-L6-v2
```

---

## LLM Model

Using local models through Ollama:

```text
mistral:7b
```

Alternative:

```text
llama3
```

---

# Why Local/Open Source Models?

Advantages:

- Completely free
- No API costs
- Privacy friendly
- Can run offline
- Good for university deployment
- Easier experimentation

---

# Recommended Folder Structure

# Backend Structure

```text
backend/
│
├── app/
│   ├── api/
│   ├── core/
│   ├── rag/
│   ├── services/
│   ├── models/
│   ├── db/
│   ├── schemas/
│   ├── middleware/
│   ├── prompts/
│   └── utils/
│
├── uploads/
├── scripts/
├── tests/
├── requirements.txt
└── main.py
```

---

# Frontend Structure

```text
frontend/
│
├── app/
├── components/
├── hooks/
├── services/
├── store/
├── types/
├── lib/
└── utils/
```

---

# RAG Pipeline

The Retrieval-Augmented Generation pipeline is the most important part of the system.

---

# Step 1 — Document Upload

Admin uploads university bylaw PDF files.

Examples:

- General Bylaws
- Examination Regulations
- Attendance Policies
- Internship Regulations
- Medical Leave Policies

---

# Step 2 — PDF Parsing

Extract text from PDFs.

Recommended Libraries:

```text
PyMuPDF
pdfplumber
unstructured
```

Extract:

- Text
- Sections
- Page Numbers
- Titles
- Metadata

---

# Step 3 — Document Cleaning

Clean extracted text:

- Remove unnecessary spaces
- Remove headers/footers
- Fix encoding issues
- Normalize formatting

---

# Step 4 — Chunking

Split documents into meaningful chunks.

Recommended:

```text
Chunk Size: 500–800 tokens
Overlap: 100–150 tokens
```

Best Practices:

- Never split mid-sentence
- Preserve section boundaries
- Preserve titles and headings
- Maintain semantic meaning

---

# Step 5 — Metadata Extraction

Store metadata with every chunk.

Example:

```json
{
  "document": "General Bylaws",
  "page": 18,
  "section": "4.2 Attendance",
  "faculty": "Engineering"
}
```

---

# Step 6 — Embedding Generation

Convert text chunks into vector embeddings.

Example:

```python
embedding = model.encode(chunk)
```

---

# Step 7 — Store in Vector Database

Store:

- Chunk text
- Embedding vector
- Metadata

Using:

```text
pgvector
```

---

# Step 8 — User Query

Student asks a question:

```text
Can I repeat a failed course?
```

---

# Step 9 — Query Embedding

Convert question into embedding vector.

---

# Step 10 — Semantic Retrieval

Retrieve top relevant chunks from vector database.

Recommended:

```text
Top K = 5
```

---

# Step 11 — Hybrid Search (IMPORTANT)

Combine:

- Semantic Search
- Keyword Search (BM25)

Why?

Semantic search alone sometimes misses exact regulation terms.

Hybrid search improves retrieval quality significantly.

---

# Step 12 — Reranking (VERY IMPORTANT)

Use reranker models to improve final retrieved chunks.

Recommended Free Reranker:

```text
BAAI/bge-reranker-base
```

Reranking improves:

- Accuracy
- Context quality
- Relevance

---

# Step 13 — Context Construction

Build prompt using retrieved chunks.

Example:

```text
Answer ONLY using the provided university regulations.

If the answer cannot be found,
say:
"I could not find this information in the university bylaws."

Context:
[Retrieved Chunks]

Question:
Can I repeat a failed course?
```

---

# Step 14 — LLM Response Generation

LLM generates grounded answer using context.

---

# Step 15 — Source Citation

Return:

- Answer
- Document name
- Page number
- Section reference

Example:

```text
Source:
General Bylaws → Section 4.2 → Page 18
```

---

# RAG Best Practices

# 1. Use Hybrid Retrieval

Always combine:

- Vector Search
- BM25 Search

This improves accuracy dramatically.

---

# 2. Add Reranking

Reranking is critical for production-quality RAG systems.

Without reranking:
- Retrieval quality becomes unstable.

---

# 3. Preserve Metadata

Always keep:

- Page numbers
- Sections
- Document names

Without metadata:
- Citations become weak
- Trust decreases

---

# 4. Prevent Hallucinations

Never allow the model to invent answers.

Prompt Rule:

```text
If the answer is not found in the provided context,
respond that the information could not be found.
```

---

# 5. Use Chunk Overlap

Overlap prevents context loss between chunks.

Recommended:

```text
100–150 token overlap
```

---

# 6. Use Smaller Focused Chunks

Very large chunks reduce retrieval quality.

Recommended:

```text
500–800 tokens
```

---

# 7. Use Conversation Memory Carefully

Store:

- Recent questions
- Chat history

But avoid:
- Sending too much history to the model

---

# 8. Add Query Expansion

Example:

```text
repeat course
retake failed subject
repeat module
```

This improves search recall.

---

# 9. Handle Scanned PDFs

Some university documents are image-based.

Use OCR:

```text
Tesseract OCR
```

---

# 10. Evaluate Retrieval Quality

Track:

- Retrieval accuracy
- Hallucination rate
- Answer correctness
- Citation correctness

---

# API Endpoints

# Chat Endpoint

```http
POST /api/chat
```

---

# Upload Documents

```http
POST /api/documents/upload
```

---

# Reindex Documents

```http
POST /api/documents/reindex
```

---

# Get Chat History

```http
GET /api/chat/history
```

---

# Authentication

Using:

```text
JWT Authentication
```

Roles:

- Student
- Admin

---

# Development Roadmap

# Phase 1 — MVP

## Goal

Create working RAG prototype.

## Features

- PDF upload
- PDF parsing
- Embeddings
- Vector search
- Basic chatbot

---

# Phase 2 — Core System

## Features

- Authentication
- Chat history
- Citations
- Multi-document support
- Better UI

---

# Phase 3 — Advanced RAG

## Features

- Hybrid retrieval
- Reranking
- Streaming responses
- Query expansion
- Better prompts

---

# Phase 4 — Production Features

## Features

- Admin dashboard
- Analytics
- Logging
- OCR support
- Multi-language support

---

# Suggested Development Timeline

# Week 1

- Setup FastAPI backend
- Setup Next.js frontend
- Setup PostgreSQL
- Setup pgvector

---

# Week 2

- Build PDF ingestion pipeline
- Build chunking system
- Build embeddings pipeline

---

# Week 3

- Build vector search
- Implement semantic retrieval
- Build RAG pipeline

---

# Week 4

- Create chatbot UI
- Add streaming responses
- Add citations

---

# Week 5

- Add authentication
- Add admin dashboard
- Add document management

---

# Week 6

- Testing
- Optimization
- Deployment

---

# Deployment

# Frontend

Recommended:

```text
Vercel
```

---

# Backend

Recommended:

```text
Railway
Render
Docker VPS
```

---

# Database

Recommended:

```text
Supabase PostgreSQL
Neon PostgreSQL
```

---

# Future Improvements

- Sinhala language support
- Tamil language support
- Voice assistant
- WhatsApp integration
- Student portal integration
- Mobile app
- Fine-tuned university model
- OCR enhancement
- Analytics dashboard

---

# Biggest Challenges

# PDF Parsing Quality

University documents are often inconsistent.

---

# Retrieval Quality

Bad chunking = bad answers.

---

# Hallucinations

LLMs may invent answers.

Need strong prompting and grounding.

---

# Cost Optimization

Embedding and model inference can become expensive at scale.

---

# Final Recommended Stack

## Frontend

- Next.js
- TypeScript
- Tailwind CSS
- shadcn/ui

---

## Backend

- FastAPI
- LangChain
- SQLAlchemy

---

## AI

- Ollama
- mistral:7b
- BAAI/bge-small-en-v1.5
- BAAI/bge-reranker-base

---

## Database

- PostgreSQL
- pgvector

---

# License

MIT License

---

# Author

University Bylaw RAG Chatbot Project

Built for helping students quickly access accurate university regulations and academic policies.