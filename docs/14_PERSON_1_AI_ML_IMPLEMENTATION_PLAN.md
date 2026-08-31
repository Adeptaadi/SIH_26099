# SIH26099 — Person 1 Implementation Plan
## AI/ML + Data Engineer

## Responsibility
Build:
```text
Raw Description → Normalization → Attribute Extraction
→ Embedding → Candidate Retrieval → Technical Comparison
→ Hybrid Score → Classification → Explanation
```

## Ownership
`data/`, `ml/`, `scripts/`

Recommended:
```text
data/
├── canonical_materials.csv
├── organization_a.csv
├── organization_b.csv
└── ground_truth.csv

ml/
├── normalization/normalizer.py
├── extraction/attribute_extractor.py
├── embeddings/embedder.py
├── retrieval/vector_search.py
├── matching/matcher.py
└── pipeline.py

scripts/generate_dataset.py
```

## Environment
Python 3.11+.
```bash
python -m venv .venv
```
Windows:
```powershell
.venv\Scripts\activate
```
Install:
```bash
pip install pandas numpy scikit-learn sentence-transformers faiss-cpu pytest
```

## Dataset
Target:
- 30–50 canonical materials
- 50–100 Org-A records
- 50–100 Org-B records
- 100–200 labelled pairs

Categories: Pipes, Valves, Bearings, Fasteners, Cables.

Create equivalent variants and hard negatives.

## Normalizer
Implement `normalize_description(text)`.

Minimum terms:
- SS/S.S. → STAINLESS STEEL
- CS/C.S. → CARBON STEEL
- SCH → SCHEDULE
- DIA → DIAMETER
- 2" → 2 IN
- 50.8 MM → 2 IN

## Attribute Extractor
Implement `extract_attributes(text)` using regex, dictionaries and rules.

Extract:
- material
- type
- size
- grade
- standard
- schedule
- pressure_class

No LLM extraction for MVP.

## Embeddings
Use `all-MiniLM-L6-v2`. Do not fine-tune.

## Retrieval
Use FAISS, default K=5.

## Matching
Implement:
```text
Final = 0.40 semantic + 0.40 attribute + 0.20 specification
```

Initial:
```text
>= 0.85 → EQUIVALENT
0.60–0.8499 → REVIEW
< 0.60 → DIFFERENT
```

Critical mismatches require explicit rules.

## Explanation
Generate from structured comparison, not an LLM.

## Final Interface
Expose:
```python
find_matches(materials_a, materials_b)
```

Return the exact `MatchResult` contract.

## Two-Day Schedule
### Day 1
0–2h: environment + dataset
2–4h: normalization
4–7h: attribute extraction
7–10h: embeddings + FAISS

### Day 2
10–13h: matcher
13–15h: classification + critical rules + explanation
15–17h: end-to-end pipeline
17–19h: evaluation
19–21h: backend integration
Remaining: bugs + threshold tuning

## Deliverables
`data/`, `ml/`, `scripts/`, `requirements.txt`, ML README.

## Do Not Build
React/UI, authentication, database CRUD, FastAPI routes, ERP/SAP integration, production deployment, LLM chatbot or fine-tuning.

## Success Criterion
Given two material sets, return ranked candidate matches with classification, confidence, matched attributes, differences and explanation.
