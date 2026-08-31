# SIH26099 — Developer Contracts

**Contract Version: 1.0**

This document is the boundary between Person 1 (AI/ML + Data) and Person 2 (Backend + Frontend). Internal implementation may change, but these external structures remain stable.

## Contract A — Material
```json
{
  "material_id": "A001",
  "organization_id": "ORG_A",
  "description": "SS PIPE 2 IN SCH40 ASTM A312 TP304"
}
```

Required: `material_id`, `organization_id`, `description`.

## Contract B — Normalized Material
```json
{
  "material_id": "A001",
  "organization_id": "ORG_A",
  "original_description": "SS PIPE 2 IN SCH40 ASTM A312 TP304",
  "normalized_description": "STAINLESS STEEL PIPE 2 IN SCHEDULE 40 ASTM A312 TP304"
}
```

## Contract C — Extracted Attributes
```json
{
  "material_id": "A001",
  "attributes": {
    "material": "STAINLESS STEEL",
    "type": "PIPE",
    "size": "2 IN",
    "grade": "TP304",
    "standard": "ASTM A312",
    "schedule": "40"
  }
}
```

Unknown values may be `null`.

## Contract D — Candidate
```json
{
  "material_a_id": "A001",
  "material_b_id": "B001",
  "semantic_score": 0.95,
  "rank": 1
}
```

## Contract E — MatchResult
```json
{
  "match_id": "MATCH001",
  "material_a_id": "A001",
  "material_b_id": "B001",
  "classification": "EQUIVALENT",
  "confidence": 0.97,
  "scores": {
    "semantic": 0.95,
    "attribute": 1.0,
    "specification": 0.95
  },
  "matched_attributes": [
    "material",
    "type",
    "size",
    "grade",
    "standard",
    "schedule"
  ],
  "differences": [],
  "explanation": "Both records describe technically equivalent materials.",
  "status": "PENDING_REVIEW"
}
```

## Contract F — Classification
Only:
- `EQUIVALENT`
- `DIFFERENT`
- `REVIEW`

## Contract G — Scores
`0.0 <= score <= 1.0`.

## Contract H — Review
```json
{"decision":"APPROVED"}
```
or:
```json
{"decision":"REJECTED"}
```

## Contract I — Common Material
```json
{
  "common_material_id": "CM001",
  "canonical_description": "STAINLESS STEEL PIPE 2 IN SCH40 ASTM A312 TP304",
  "source_materials": [
    {"organization_id": "ORG_A", "material_id": "A001"},
    {"organization_id": "ORG_B", "material_id": "B001"}
  ]
}
```

## Contract J — Upload Response
```json
{
  "upload_id": "UP001",
  "organization_id": "ORG_A",
  "records_processed": 100,
  "records_rejected": 2,
  "status": "SUCCESS"
}
```

## Contract K — Matching Request
```json
{
  "organization_a": "ORG_A",
  "organization_b": "ORG_B"
}
```

## Contract L — Matching Response
```json
{
  "job_id": "JOB001",
  "status": "COMPLETED",
  "matches_found": 42
}
```

## Contract M — Ownership
### Person 1
`data/`, `ml/`, `scripts/`

### Person 2
`backend/`, `frontend/`

### Shared
`docs/`, `README.md`

## Contract N — Integration Rule
Person 2 interacts with the ML layer only through the agreed interface. Person 1 does not depend on frontend implementation details.

## Contract O — Breaking Changes
For changes to fields, types, classifications, routes or required data:
1. Update this contract.
2. Update API specification.
3. Update implementation.
4. Update tests.
5. Inform the other developer.

## Contract P — Version
MVP targets Contract Version 1.0.

## Contract Q — Evaluation Metrics Response
```json
{
  "total_pairs": 150,
  "accuracy": 0.9867,
  "precision": 1.0,
  "recall": 0.9333,
  "f1_score": 0.9655,
  "hard_negative_accuracy": 1.0,
  "confusion_matrix": {
    "true_positives": 28,
    "false_positives": 0,
    "true_negatives": 120,
    "false_negatives": 2
  }
}
```

## Contract R — Ablation Study Response
```json
{
  "methods": [
    {"name": "Exact String Matching", "precision": 1.0, "recall": 0.45, "f1_score": 0.62},
    {"name": "Semantic Similarity Only", "precision": 0.78, "recall": 0.96, "f1_score": 0.86},
    {"name": "Semantic + Attribute Matching", "precision": 0.88, "recall": 0.94, "f1_score": 0.91},
    {"name": "Hybrid Pipeline (With Rules)", "precision": 1.0, "recall": 0.93, "f1_score": 0.97}
  ]
}
```

## Contract S — Pipeline Latency Metrics
```json
{
  "latency": {
    "normalization_ms": 12.5,
    "extraction_ms": 25.1,
    "embedding_ms": 140.2,
    "retrieval_ms": 5.4,
    "matching_ms": 18.8,
    "total_ms": 202.0
  }
}
```

