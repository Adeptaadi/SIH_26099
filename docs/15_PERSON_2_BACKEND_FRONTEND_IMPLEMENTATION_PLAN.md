# SIH26099 — Person 2 Implementation Plan
## Backend + Frontend Engineer

## Responsibility
Build:
```text
Upload → Process → Match → Dashboard → Inspect
→ Approve/Reject → Common Material
```

## Ownership
`backend/`, `frontend/`

## Backend Structure
```text
backend/app/
├── main.py
├── routes/
│   ├── health.py
│   ├── materials.py
│   ├── matching.py
│   └── reviews.py
├── schemas/
├── services/
└── db/
    ├── database.py
    └── models.py
```

## Frontend Structure
```text
frontend/src/
├── pages/
│   ├── Upload.jsx
│   ├── Dashboard.jsx
│   ├── MatchDetails.jsx
│   └── CommonMaterials.jsx
├── components/
├── services/api.js
└── App.jsx
```

## Environment
Backend:
```bash
pip install fastapi uvicorn sqlalchemy pandas python-multipart
uvicorn app.main:app --reload
```

Frontend: React + Vite.

## Database
Use SQLite for the MVP:
- materials
- matches
- reviews
- common_materials

## APIs
Implement:
- GET `/api/health`
- POST `/api/materials/upload`
- POST `/api/matching/run`
- GET `/api/matches`
- GET `/api/matches/{match_id}`
- POST `/api/matches/{match_id}/review`
- GET `/api/common-materials`

## ML Integration
Call Person 1's:
```python
find_matches(materials_a, materials_b)
```

Do not reproduce ML logic in the backend.

## Upload
Accept:
- file
- organization_id

Validate CSV, required columns, duplicates, empty files and invalid rows.

## Review
Accept:
```json
{"decision":"APPROVED"}
```
or:
```json
{"decision":"REJECTED"}
```

Persist decision and update status.

## Common Material
After an approved equivalent match, create a common-material record.

## UI
Routes:
- `/upload`
- `/dashboard`
- `/matches/:id`
- `/common-materials`

Upload page: two CSV inputs + Run Matching.

Dashboard: total, equivalent, review, different + result table.

Match detail: both descriptions, attribute comparison, confidence, scores, explanation and review actions.

Common materials: ID, canonical description, attributes and source records.

## API Layer
Create `frontend/src/services/api.js` with:
- uploadMaterials()
- runMatching()
- getMatches()
- getMatch()
- reviewMatch()
- getCommonMaterials()

## Two-Day Schedule
### Day 1
0–2h: FastAPI + SQLite + health
2–5h: material model + upload + validation
5–7h: React + routing + upload page
7–10h: dashboard + results

### Day 2
10–13h: matching API + ML integration
13–15h: match list/detail APIs
15–17h: match-detail UI
17–19h: review + common materials
19–21h: end-to-end integration
Remaining: UI polish + bugs

## Do Not Build
Authentication, RBAC, multi-tenancy, PostgreSQL, Redis, Kafka, background jobs, ERP/SAP integration, mobile app, admin panel or advanced analytics.

## Success Criterion
A user can upload two organization files, run matching, inspect results, understand reasoning, approve/reject a match and see approved records as common materials.
