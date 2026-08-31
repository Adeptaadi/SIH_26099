# SIH26099 — Person 2 (Backend + Frontend) Implementation Plan (Upgrades)
## Upgrade Focus: Rich UI Visualizations, Dynamic API metrics, and Retrieval Demonstrations

This document details the step-by-step implementation plan for **Person 2** to integrate and visualize the new pipeline metrics, ablation studies, and technical explainability features.

---

## 1. Responsibilities & Deliverables
Person 2 is responsible for:
1. Creating Backend endpoints `/api/evaluation/metrics`, `/api/evaluation/ablation`, and `/api/demo/hard-negatives`.
2. Enhancing the **Match Details Page** to show:
   - A side-by-side attribute comparison table (Org A vs Org B vs Normalization status).
   - An interactive "Decision Boundary Slider" indicating the hybrid score against thresholds.
   - The latency breakdown chart.
3. Building an **Evaluation Dashboard** page featuring:
   - Performance metrics cards (Accuracy, Precision, Recall, F1).
   - A styled 3x3 or 2x2 Confusion Matrix.
   - An Ablation Study comparison table comparing the 4 matching methods.
4. Implementing the **Hard Negative Demo Page** to showcase how the system handles critical parameter overrides.

---

## 2. Component Modifications

### A. Backend Route Extensions
Expose new endpoints inside `backend/app/routes/`:
* `GET /api/evaluation/metrics`: Retrieves metrics from database matches and ground truth using Person 1's evaluation engine.
* `GET /api/evaluation/ablation`: Runs the 4 ablation methods and returns comparative statistics.
* `GET /api/demo/hard-negatives`: Pulls hard negative query matches (e.g. grade mismatches, size mismatches) from the DB to show on the demo page.

### B. Frontend Page Enhancements
* **Match Details page (`MatchDetails.jsx`)**:
  - Replace the text-based summary with a comparative table.
  - Add a visual threshold timeline showing the score pointer.
  - Include a latency bar breakdown using pure CSS bars or simple flex graphs.
* **Evaluation Dashboard (`Dashboard.jsx` or new `Evaluation.jsx` page)**:
  - Grid of metrics.
  - Interactive grid representing the Confusion Matrix.
  - Table comparison for the Ablation Study.
* **Hard Negative Demo (`HardNegativesDemo.jsx`)**:
  - A dashboard presenting the "Semantic vs Technical Mismatch" cases.

---

## 3. Step-by-Step Implementation Steps

### Step 1: Implement Backend Endpoints
* **Files**: `backend/app/routes/matching.py` (or new route file)
* Build the `/api/evaluation/metrics` route:
  - Fetches all database matches and references `data/ground_truth/ground_truth.csv`.
  - Invokes `compute_evaluation_metrics` and returns the JSON payload.
* Build the `/api/evaluation/ablation` route:
  - Invokes the ablation runner and returns scores.
* Build the `/api/demo/hard-negatives` route:
  - Filters matches in the DB where `classification == 'DIFFERENT'` and `is_overridden == True` and returns them.

### Step 2: Implement Side-by-Side Comparison UI
* **File**: `frontend/src/pages/MatchDetails.jsx`
* Create a table comparing attributes from Org A and Org B:
  - Columns: Attribute Name, Org A Value, Org B Value, Compatibility Status (✓ Match, ✓ Normalized Match, ✗ Mismatch).
* Render a custom slider bar showing boundaries:
  - Boundaries at 0.60 and 0.85. Place the candidate score on the slider using colors (red, orange, green).

### Step 3: Implement Confusion Matrix and Ablation Visuals
* **File**: `frontend/src/pages/Dashboard.jsx` (add tabs or link to a new page)
* Add a Confusion Matrix grid:
  - Renders a styled 2x2 grid representing TP, FP, TN, FN with counts and color density.
* Render the Ablation Table:
  - Table headers: Method, Precision, Recall, F1-Score.
  - Highlight the Hybrid System method row.

---

## 4. Verification Plan
* Start backend server: `uvicorn app.main:app` and curl the `/api/evaluation/metrics` endpoint.
* Open Vite frontend: `npm run dev`, navigate to the pages, and verify tables, charts, and values are fully dynamic and match.
