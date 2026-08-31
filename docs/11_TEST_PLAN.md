# SIH26099 — Test Plan

## Data Tests
- Valid CSV → success
- Missing description → validation error
- Duplicate ID → duplicate reported
- Empty file → invalid file
- Invalid CSV → clear error

## Normalization
```text
SS → STAINLESS STEEL
S.S. → STAINLESS STEEL
CS → CARBON STEEL
SCH → SCHEDULE
2" → 2 IN
50.8 MM → 2 IN
```

## Attribute Tests
Verify material, type, size, grade, standard and schedule extraction.

## Matching Tests
- Exact description → EQUIVALENT
- Different wording, same specification → EQUIVALENT
- Equivalent unit variation → EQUIVALENT
- TP304 vs TP316 → DIFFERENT or REVIEW
- 2 IN vs 3 IN → DIFFERENT or REVIEW

## API Tests
Test all endpoints in `06_API_SPECIFICATION.md`.

## UI Tests
Test upload, matching, dashboard, details, approval, rejection and common materials.

## End-to-End
```text
Upload A → Upload B → Run Matching → Results
→ Match Detail → Review → Common Material
```
