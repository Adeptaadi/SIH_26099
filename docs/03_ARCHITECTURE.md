# SIH26099 — System Architecture

## Overview
```text
                 React Frontend
                       │
                    REST API
                       ▼
                 FastAPI Backend
                       │
          ┌────────────┼────────────┐
          ▼            ▼            ▼
      Data Service  Matching     Review
                         │
                         ▼
                    ML Pipeline
                         │
               ┌─────────┴─────────┐
               ▼                   ▼
          Embeddings             Rules
               │                   │
               └─────────┬─────────┘
                         ▼
                       FAISS
                         │
                         ▼
                    SQLite DB
```

## Technology
- Frontend: React, Vite, CSS/Tailwind
- Backend: Python, FastAPI, Pydantic, SQLAlchemy
- AI/ML: Sentence Transformers, FAISS, NumPy, regex/rules
- Storage: SQLite and CSV

## Processing
```text
Raw Description
→ Normalization
→ Attribute Extraction
→ Embedding
→ FAISS Top-K
→ Technical Comparison
→ Hybrid Score
→ Classification
→ Explanation
```

## Responsibility
### Person 1
Normalization, extraction, embeddings, retrieval, matching and explanation.

### Person 2
Upload, validation, persistence, API, review and UI.

## Data Source Abstraction
```text
CSV / Database / ERP / API
          ↓
    Material Schema
          ↓
      ML Pipeline
```
