# SIH26099 — Git Collaboration

## Branches
```text
main
├── feature/ml-engine
└── feature/backend-ui
```

## Person 1
Branch: `feature/ml-engine`
Primary: `data/`, `ml/`, `scripts/`

## Person 2
Branch: `feature/backend-ui`
Primary: `backend/`, `frontend/`

## Shared
`docs/`, `README.md`

## Commit Convention
Use:
- `feat:`
- `fix:`
- `refactor:`
- `test:`
- `docs:`

## Pull Requests
No direct commits to `main`.

```text
Feature branch → Commit → Push → PR → Review → Merge
```

## Contract Rule
Shared contracts must not be changed silently.

## Integration
Integrate early. Do not wait for both sides to be completely finished.

## Golden Rule
`main` must always remain runnable.
