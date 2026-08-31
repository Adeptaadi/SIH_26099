# SIH26099 — Person 1 (AI/ML + Data) Implementation Plan (Upgrades)
## Upgrade Focus: Explainability, Retrieval Rigor, and Evaluation Dashboards

This document details the step-by-step implementation plan for **Person 1** to incorporate technical explainability, ablation statistics, evaluation metrics, and latency instrumentation into the matching system.

---

## 1. Responsibilities & Deliverables
Person 1 is responsible for:
1. Instrumenting the pipeline with dynamic latency tracking for each execution phase.
2. Building the evaluation engine to compute Accuracy, Precision, Recall, F1 Score, and a Confusion Matrix on the fly.
3. Implementing the ablation study runner comparing the performance of 4 distinct matching methods.
4. Structuring a dedicated hard-negatives query set to prove technical robustness.
5. Exposing these modules through helper functions consumed by Person 2's backend services.

---

## 2. Component Modifications

### A. Pipeline Latency Instrumentation
We will modify `ml/pipeline.py` to record execution timestamps using `time.perf_counter()`.
Expose a breakdown dictionary in the match results:
```python
latency_metrics = {
    "normalization_time": 0.0,
    "extraction_time": 0.0,
    "embedding_time": 0.0,
    "retrieval_time": 0.0,
    "matching_time": 0.0,
    "total_time": 0.0
}
```

### B. Evaluation Engine
We will implement a helper class/function `ml/evaluation/evaluator.py`:
* **Function**: `compute_evaluation_metrics(db_matches, ground_truth)`
* **Output**:
  - Precision, Recall, F1-Score, and Accuracy.
  - **Confusion Matrix counts**:
    - True positives, True negatives, False positives, False negatives.
    - True `REVIEW` and `DIFFERENT` mappings.

### C. Ablation Runner
We will implement an ablation configuration engine in `ml/matching/ablation.py`:
* Runs the matching dataset through 4 pipeline methods:
  1. **Method 1 (Exact Match)**: Case-insensitive raw string matching.
  2. **Method 2 (Semantic Only)**: Threshold checks based strictly on SentenceTransformer cosine similarity.
  3. **Method 3 (Semantic + Basic Attributes)**: Semantic score + attribute matching without critical overrides.
  4. **Method 4 (Hybrid System)**: Our full pipeline (Semantic + Attributes + Specification Rules + Critical overrides).
* Returns a dictionary comparing the F1-scores, Precisions, and Recalls of all 4 methods.

---

## 3. Step-by-Step Implementation Steps

### Step 1: Add Latency Instrumentations
* **File**: `ml/pipeline.py`
* Instrument the `find_matches` pipeline:
  - Time the normalization step.
  - Time the `MaterialEmbedder.embed` calls.
  - Time the `VectorIndex.search` calls.
  - Time the detailed `match_materials` calls.
  - Return the latency breakdown dictionary in the pipeline response.

### Step 2: Build the Evaluation Engine
* **File**: `ml/evaluation/evaluator.py`
* Build the metrics calculator. Compare the predicted classifications from the database against labels in `ground_truth.csv`:
  - Map predicted `EQUIVALENT` and `REVIEW` to positive, `DIFFERENT` to negative (or build a 3x3 multi-class confusion matrix).
  - Calculate actual counts for: `True Positive`, `False Positive`, `True Negative`, `False Negative`.

### Step 3: Implement the Ablation Study Runner
* **File**: `ml/matching/ablation.py`
* Write the ablation runner that executes the 4 configurations on the evaluation pairs:
  - Method 1: Matches only if `normalize_description(a) == normalize_description(b)`.
  - Method 2: Matches if `semantic_score >= 0.85` (ignores attributes/mismatches).
  - Method 3: Matches if `0.5 * semantic_score + 0.5 * attribute_score >= 0.85`.
  - Method 4: Full hybrid pipeline with critical attribute overrides.

### Step 4: Write Unit Tests
* **File**: `tests/test_evaluation.py` and `tests/test_ablation.py`
* Verify that:
  - Latency tracking does not raise exceptions.
  - Evaluation metrics are computed mathematically correctly.
  - Ablation runner returns scores for all 4 configurations.

---

## 4. Verification Plan
* Run `python -m pytest tests/` to confirm all code compiles and passes test verification.
* Execute `python -m scripts.evaluate_model` to verify that performance values compile.
