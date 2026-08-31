# SIH26099 — Product Requirements Document

## Product
AI-Powered Material Master Harmonization and Equivalence Detection.

## Problem
Organizations may describe the same technically equivalent material using different wording, abbreviations, units, ordering and terminology. Exact-string matching therefore misses valid equivalences.

Example:
- Org A: `SS PIPE 2 IN SCH40 ASTM A312 TP304`
- Org B: `STAINLESS STEEL SEAMLESS PIPE 50.8 MM SCHEDULE 40 ASTM A312 GRADE 304`

## Objective
The MVP shall:
1. Accept material records from two organizations.
2. Normalize descriptions.
3. Extract technical attributes.
4. Generate semantic embeddings.
5. Retrieve likely candidates.
6. Calculate a hybrid equivalence score.
7. Classify pairs as `EQUIVALENT`, `DIFFERENT`, or `REVIEW`.
8. Explain matching/differing attributes.
9. Support human approval/rejection.
10. Display approved records as common materials.

## MVP Flow
```text
Upload A + B → Validate → Normalize → Extract → Embed
→ Retrieve → Hybrid Match → Classify → Explain
→ Human Review → Common Material
```

## Users
- Procurement/material master-data teams
- Inventory teams
- Data governance teams
- Technical procurement officers

## Functional Requirements
- CSV upload and validation
- Text/unit normalization
- Technical attribute extraction
- Semantic candidate retrieval
- Hybrid matching
- Classification and explanation
- Human review
- Common-material grouping

## Non-Functional Requirements
- Simple local deployment
- Explainable decisions
- Modular AI/backend boundary
- MVP-scale processing of roughly 100–200 records
- Replaceable data source

## Out of Scope
Authentication, RBAC, ERP/SAP integration, distributed processing, Kafka, Redis, Kubernetes, fine-tuning, production MLOps and advanced knowledge graphs.

## Future Vision
Support multiple organizations, real enterprise data, ERP/API ingestion, scalable processing, audit trails, human-in-the-loop learning, analytics and production MLOps.
