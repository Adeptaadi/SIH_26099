# SIH26099 — PROJECT STRUCTURE

**Project:** AI-Powered Material Master Harmonization and Equivalence Detection  
**Version:** MVP v1.0  
**Development Team:** 2 Members

---

## 1. Complete Repository Structure

```text
SIH26099/
│
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── routes/
│   │   │   ├── __init__.py
│   │   │   ├── health.py
│   │   │   ├── materials.py
│   │   │   ├── matching.py
│   │   │   ├── reviews.py
│   │   │   └── common_materials.py
│   │   ├── schemas/
│   │   │   ├── __init__.py
│   │   │   ├── material.py
│   │   │   ├── match.py
│   │   │   ├── review.py
│   │   │   └── common_material.py
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── material_service.py
│   │   │   ├── matching_service.py
│   │   │   ├── review_service.py
│   │   │   └── common_material_service.py
│   │   ├── db/
│   │   │   ├── __init__.py
│   │   │   ├── database.py
│   │   │   ├── models.py
│   │   │   └── seed.py
│   │   └── core/
│   │       ├── __init__.py
│   │       └── config.py
│   ├── tests/
│   │   ├── test_health.py
│   │   ├── test_materials.py
│   │   ├── test_matching.py
│   │   └── test_reviews.py
│   ├── requirements.txt
│   └── README.md
│
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── assets/
│   │   ├── components/
│   │   │   ├── Navbar.jsx
│   │   │   ├── StatCard.jsx
│   │   │   ├── MatchTable.jsx
│   │   │   ├── AttributeComparison.jsx
│   │   │   ├── ConfidenceBadge.jsx
│   │   │   ├── ReviewButtons.jsx
│   │   │   └── Loading.jsx
│   │   ├── pages/
│   │   │   ├── Upload.jsx
│   │   │   ├── Dashboard.jsx
│   │   │   ├── MatchDetails.jsx
│   │   │   └── CommonMaterials.jsx
│   │   ├── services/
│   │   │   └── api.js
│   │   ├── hooks/
│   │   │   └── useMatches.js
│   │   ├── utils/
│   │   │   └── formatters.js
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   └── index.css
│   ├── package.json
│   ├── vite.config.js
│   └── README.md
│
├── ml/
│   ├── __init__.py
│   ├── normalization/
│   │   ├── __init__.py
│   │   ├── normalizer.py
│   │   └── dictionaries.py
│   ├── extraction/
│   │   ├── __init__.py
│   │   ├── attribute_extractor.py
│   │   ├── patterns.py
│   │   └── dictionaries.py
│   ├── embeddings/
│   │   ├── __init__.py
│   │   └── embedder.py
│   ├── retrieval/
│   │   ├── __init__.py
│   │   └── vector_search.py
│   ├── matching/
│   │   ├── __init__.py
│   │   ├── matcher.py
│   │   ├── scorer.py
│   │   ├── classifier.py
│   │   └── explanation.py
│   ├── pipeline.py
│   └── config.py
│
├── data/
│   ├── raw/
│   │   ├── organization_a.csv
│   │   └── organization_b.csv
│   ├── processed/
│   │   ├── normalized_a.csv
│   │   └── normalized_b.csv
│   ├── ground_truth/
│   │   └── ground_truth.csv
│   └── canonical/
│       └── canonical_materials.csv
│
├── scripts/
│   ├── generate_dataset.py
│   ├── preprocess_data.py
│   └── evaluate_model.py
│
├── tests/
│   ├── test_normalization.py
│   ├── test_extraction.py
│   ├── test_embeddings.py
│   ├── test_retrieval.py
│   ├── test_matching.py
│   └── test_pipeline.py
│
├── docs/
│   ├── 01_PRD.md
│   ├── 02_MVP_SCOPE.md
│   ├── 03_ARCHITECTURE.md
│   ├── 04_DATA_SPECIFICATION.md
│   ├── 05_AI_MATCHING_SPECIFICATION.md
│   ├── 06_API_SPECIFICATION.md
│   ├── 07_CONTRACTS.md
│   ├── 08_UI_SPECIFICATION.md
│   ├── 09_DATABASE_SPECIFICATION.md
│   ├── 10_EVALUATION.md
│   ├── 11_TEST_PLAN.md
│   ├── 12_GIT_COLLABORATION.md
│   ├── 13_DEMO_SCRIPT.md
│   ├── 14_PERSON_1_AI_ML_IMPLEMENTATION_PLAN.md
│   ├── 15_PERSON_2_BACKEND_FRONTEND_IMPLEMENTATION_PLAN.md
│   └── 16_PROJECT_STRUCTURE.md
│
├── .gitignore
├── README.md
└── requirements.txt
```

---

## 2. Ownership

### Person 1 — AI/ML + Data

Primary ownership:

```text
ml/
data/
scripts/
tests/test_normalization.py
tests/test_extraction.py
tests/test_embeddings.py
tests/test_retrieval.py
tests/test_matching.py
tests/test_pipeline.py
```

Responsible for:
- Dataset generation
- Data preprocessing
- Normalization
- Attribute extraction
- Embeddings
- FAISS retrieval
- Matching
- Scoring
- Classification
- Explanation
- ML evaluation

### Person 2 — Backend + Frontend

Primary ownership:

```text
backend/
frontend/
backend/tests/
```

Responsible for:
- CSV upload
- API
- Database
- Backend services
- Review system
- Common-material storage
- React UI
- Dashboard
- Match details
- API integration

---

## 3. Shared Files

Both developers can modify:

```text
README.md
requirements.txt
.gitignore
docs/
```

The most important shared document is:

```text
docs/07_CONTRACTS.md
```

It defines the interface between Person 1 and Person 2.

---

## 4. Critical Integration Boundary

```text
                PERSON 1
                    │
                    │ MatchResult
                    ▼
             ┌─────────────┐
             │ ML INTERFACE│
             └─────────────┘
                    │
                    ▼
                PERSON 2
```

Person 1 exposes:

```python
find_matches(materials_a, materials_b)
```

The result must follow Contract v1.0 in `docs/07_CONTRACTS.md`.

Person 2 consumes the result and must not duplicate ML logic.

---

## 5. Data Flow

```text
Organization A ──┐
                 ├──> Person 1 ML Pipeline
Organization B ──┘
                         │
                         ├── Normalize
                         ├── Extract Attributes
                         ├── Embeddings
                         ├── FAISS Retrieval
                         ├── Hybrid Matching
                         └── Explanation
                                  │
                                  ▼
                              MatchResult
                                  │
                                  ▼
                              FastAPI
                                  │
                                  ▼
                               SQLite
                                  │
                                  ▼
                              React UI
                                  │
                                  ▼
                            Human Review
                                  │
                                  ▼
                         Common Materials
```

---

## 6. Development Order

### Phase 1 — Repository Setup

Both developers:
1. Create repository.
2. Create branches.
3. Create folder structure.
4. Create README and `.gitignore`.
5. Freeze Contract v1.0.

### Phase 2 — Person 1

```text
Dataset
  ↓
Normalization
  ↓
Attribute Extraction
  ↓
Embeddings
  ↓
FAISS
  ↓
Matcher
  ↓
MatchResult
```

### Phase 3 — Person 2

Build independently with mock `MatchResult` objects:
- FastAPI
- SQLite
- Upload
- Dashboard
- Match details
- Review
- Common materials

### Phase 4 — Integration

```text
Person 1 MatchResult
        ↓
     FastAPI
        ↓
      SQLite
        ↓
     React UI
```

---

## 7. Two-Day Prototype Priority

### Day 1

Person 1:
```text
Dataset
Normalization
Extraction
Basic matching
```

Person 2:
```text
FastAPI
SQLite
Upload API
React Upload + Dashboard
```

### Day 2

Person 1:
```text
Embeddings
FAISS
Hybrid Score
Explanation
```

Person 2:
```text
Match Details
Review
Common Materials
Integration
```

---

## 8. Temporary Simplification

If time is limited, Person 1 may temporarily combine the ML modules inside:

```text
ml/pipeline.py
```

Later refactor into the final module structure.

Person 2 may similarly start with fewer backend files.

**Do not change the ML/API contract to accommodate temporary implementation shortcuts.**

---

## 9. Minimum First Working Demo

```text
SIH26099/
├── backend/
│   └── app/
├── frontend/
│   └── src/
├── ml/
│   ├── pipeline.py
│   ├── normalization/
│   ├── extraction/
│   ├── embeddings/
│   ├── retrieval/
│   └── matching/
├── data/
│   ├── raw/
│   └── ground_truth/
├── scripts/
│   └── generate_dataset.py
├── docs/
│   └── 07_CONTRACTS.md
└── README.md
```

Everything else can be added after the first end-to-end flow works.

---

## 10. Final MVP Architecture

```text
                    ┌──────────────┐
                    │    React     │
                    │   Frontend   │
                    └──────┬───────┘
                           │
                          REST
                           │
                    ┌──────▼───────┐
                    │   FastAPI    │
                    │   Backend    │
                    └──────┬───────┘
                           │
              ┌────────────┼────────────┐
              ▼            ▼            ▼
          Materials      Matching      Review
                           │
                           ▼
                      ML Pipeline
                           │
                    ┌──────┴──────┐
                    ▼             ▼
                Embeddings      Rules
                    │             │
                    └──────┬──────┘
                           ▼
                         FAISS
                           │
                           ▼
                        SQLite
                           │
                           ▼
                  Common Materials
```

---

## 11. Architectural Rule

The MVP has three major application layers:

```text
PRESENTATION
     ↓
APPLICATION
     ↓
INTELLIGENCE
```

### Presentation

```text
frontend/
```

### Application

```text
backend/
```

### Intelligence

```text
ml/
```

### Data

```text
data/
```

This separation should remain when the MVP is expanded into the full SIH solution.
