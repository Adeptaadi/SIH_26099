# SIH26099 — AI Matching Specification

## Objective
Determine whether two material descriptions are technically equivalent, clearly different, or ambiguous enough for human review.

## Pipeline
```text
Description → Normalization → Attribute Extraction
→ Embedding → Candidate Retrieval → Attribute Comparison
→ Hybrid Scoring → Classification → Explanation
```

## Normalization
Examples:
- `SS`, `S.S.` → `STAINLESS STEEL`
- `CS`, `C.S.` → `CARBON STEEL`
- `SCH` → `SCHEDULE`
- `DIA` → `DIAMETER`
- `2"` → `2 IN`
- `50.8 MM` → `2 IN`

Only normalize transformations that preserve technical meaning.

## Attributes
Possible attributes:
`material`, `type`, `size`, `grade`, `standard`, `schedule`, `pressure_class`, `diameter`, `length`, `voltage`.

Missing attributes are `null`.

## Embeddings
Use a pretrained sentence-transformer. A lightweight starting point is `all-MiniLM-L6-v2`. No fine-tuning for the MVP.

## Retrieval
Use FAISS and retrieve Top-K candidates. Default K = 5.

## Hybrid Score
```text
Final Score =
0.40 × Semantic Score
+ 0.40 × Attribute Score
+ 0.20 × Specification Score
```

Scores are between 0 and 1.

## Classification
```text
score >= 0.85       → EQUIVALENT
0.60 <= score < .85 → REVIEW
score < 0.60        → DIFFERENT
```

Critical technical mismatches may override the numerical score.

## Critical Attributes
Material, size, grade, standard, schedule and pressure class require special handling.

## Explanation
Generate explanations from structured comparisons, not an LLM, for the MVP.

Example:
`Both descriptions have the same material, type, size, grade, standard and schedule.`

Hard negative:
`The descriptions are similar, but the material grade differs: TP304 vs TP316.`

## Output
Return the exact `MatchResult` defined in `07_CONTRACTS.md`.
