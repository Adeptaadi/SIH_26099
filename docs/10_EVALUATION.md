# SIH26099 — Evaluation Plan

## Dataset
Use the generated ground-truth dataset.

## Test Categories
- Positive: different descriptions, same technical material
- Hard negative: similar wording, important technical mismatch
- Negative: clearly different materials

## Metrics
- Accuracy
- Precision
- Recall
- F1 score

## Hard-Negative Evaluation
Report grade, size, material, standard and schedule mismatch performance.

## Objective
Demonstrate that the system:
1. Matches different wording when specifications agree.
2. Rejects similar wording when important specifications differ.
3. Sends uncertain cases to human review.

## Reporting
Use actual measured values only.
```text
Test pairs: 150
Accuracy: XX%
Precision: XX%
Recall: XX%
F1: XX%
Hard-negative accuracy: XX%
```
