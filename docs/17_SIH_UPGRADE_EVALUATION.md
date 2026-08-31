# SIH26099 — SIH Judge Evaluation & Upgrades Proposal

This document outlines the proposed Phase 2 upgrades to enhance the defensibility and technical depth of the matching pipeline for SIH evaluation.

---

## 1. Upgrade Strategic Impact

Smart India Hackathon (SIH) judges assess systems on explainability, scientific rigor, and robustness against edge cases. This upgrade focuses on shifting the MVP from a "black-box AI" to a transparent, auditable engineering system.

```
                  MATERIAL A
                      │
                      ▼
               NORMALIZATION
                      │
                      ▼
              ATTRIBUTE EXTRACTION
                      │
                      ▼
                 EMBEDDING
                      │
                      ▼
                 FAISS TOP-K
                      │
             ┌────────┴────────┐
             ▼                 ▼
       Candidate 1       Candidate 2
             │                 │
             ▼                 ▼
      TECHNICAL CHECK     TECHNICAL CHECK
             │                 │
             └────────┬────────┘
                      ▼
                HYBRID SCORE
                      │
          ┌───────────┼───────────┐
          ▼           ▼           ▼
      EQUIVALENT    REVIEW     DIFFERENT
          │           │
          │           ▼
          │      HUMAN REVIEW
          │           │
          └─────┬─────┘
                ▼
          COMMON MATERIAL
```

---

## 2. The 7 Selected Upgrades

### Tier 1 — Core Demonstration Upgrades
1. **Explainable Match Detail**:
   - Displays a side-by-side comparative table of extracted parameters (material, type, size, standard, etc.) and highlights normalization flags. Shows the exact weighted breakdown of semantic similarity, attribute compatibility, and specification scores.
2. **Hard Negative Demonstration**:
   - A dedicated page showcasing "Why Semantic Similarity is Insufficient" (e.g. comparing `TP304` and `TP316` steel pipes which have 95% semantic similarity but are distinct products). Demonstrates how the system's critical attribute overrides catch these mismatches.
3. **Top-K Retrieval Visibility**:
   - Renders the retrieval rank list from FAISS vector search. Proves to judges that the retrieval architecture scales efficiently ($O(N \log K)$) instead of performing slow, exhaustive pairwise comparisons.
4. **Evaluation Dashboard**:
   - Displays actual measured metrics (Accuracy, Precision, Recall, F1 Score) and renders a visual 2x2 Confusion Matrix generated dynamically from database match statuses against the ground truth labels.

### Tier 2 — Engineering Depth Upgrades
5. **Ablation Study Dashboard**:
   - Presents a table comparing performance across four implementation iterations:
     - Exact String Matching
     - Semantic Similarity Only
     - Semantic + Attribute Match
     - Full Hybrid Pipeline (with overrides)
   - Proves statistically that the hybrid system reduces false equivalence errors.
6. **Human-in-the-loop Learning Flowchart**:
   - Visualizes the data provenance and active learning loop (User Approval/Rejection $\rightarrow$ Database Feedback Log $\rightarrow$ Labeled retrain dataset).
7. **Performance & Latency Instrumentations**:
   - Measures and visualizes processing, embedding, index searching, and rule execution times to demonstrate system performance awareness.

---

## 3. Verification Plan
* Validate all APIs and UI charts on local servers:
  - Backend: `http://localhost:8000/api`
  - Frontend: `http://localhost:3000/`
