# SIH26099 — MVP Scope

## Must Have
### Data
- Generated realistic dataset
- Organization A and B records
- Ground truth
- CSV support

### AI
- Text normalization
- Unit normalization for used examples
- Attribute extraction
- Sentence embeddings
- FAISS candidate retrieval
- Attribute comparison
- Hybrid scoring
- Classification
- Explanation

### Application
- CSV upload
- Matching execution
- Results dashboard
- Match detail
- Human approval/rejection
- Common-material view

### Storage
- SQLite
- Materials
- Matches
- Reviews
- Common materials

## Should Have
- Loading indicator
- Error messages
- Search/filter
- Confidence display
- Match statistics
- Evaluation metrics

## Not Now
Authentication, RBAC, multi-tenancy, ERP/SAP integration, real government APIs, production deployment, distributed processing, Redis/Kafka, fine-tuning, knowledge graph and advanced MLOps.

## Dataset Target
- 30–50 canonical materials
- 50–100 Org-A records
- 50–100 Org-B records
- 100–200 labelled pairs

Categories: Pipes, Valves, Bearings, Fasteners, Cables.

## Definition of Done
```text
CSV A + CSV B → Upload → Normalize → Extract → Embed
→ Retrieve → Match → Classify → Explain → Review
→ Common Material
```
