# SIH26099 — AI Material Master Harmonization

## Problem
Organizations may describe technically equivalent materials differently. This project detects potential equivalence using normalization, technical attributes and semantic similarity.

## MVP
```text
Upload A + B → Normalize → Extract → Semantic Retrieval
→ Hybrid Matching → Equivalent / Review / Different
→ Human Review → Common Material
```

## Tech Stack
- React + Vite
- FastAPI
- Python
- Sentence Transformers
- FAISS
- SQLite
- Pandas

## Repository
```text
backend/
frontend/
data/
ml/
scripts/
docs/
```

## Documentation
See `docs/` for PRD, MVP scope, architecture, data, AI, API, contracts, UI, database, evaluation, testing, Git, demo and individual implementation plans.

## Run Backend
```bash
cd backend
uvicorn app.main:app --reload
```

## Run Frontend
```bash
cd frontend
npm install
npm run dev
```

## Generate Dataset
```bash
python scripts/generate_dataset.py
```

## Tests
```bash
pytest
```

## Important
Generated data is used for controlled demonstration. Real data sources can be integrated later without changing the core material contract.
