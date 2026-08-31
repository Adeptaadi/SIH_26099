# SIH26099 — API Specification

## Base Path
`/api`

## GET /health
```json
{"status":"ok"}
```

## POST /materials/upload
Multipart fields:
- `file`
- `organization_id`

Response:
```json
{
  "upload_id": "UP001",
  "organization_id": "ORG_A",
  "records_processed": 100,
  "records_rejected": 2,
  "status": "SUCCESS"
}
```

## POST /matching/run
Request:
```json
{
  "organization_a": "ORG_A",
  "organization_b": "ORG_B"
}
```

Response:
```json
{
  "job_id": "JOB001",
  "status": "COMPLETED",
  "matches_found": 42
}
```

## GET /matches
Returns match summaries.

## GET /matches/{match_id}
Returns the complete MatchResult.

## POST /matches/{match_id}/review
Request:
```json
{"decision":"APPROVED"}
```
Allowed: `APPROVED`, `REJECTED`.

## GET /common-materials
Returns approved common-material groups.

## Error Format
```json
{
  "error": {
    "code": "INVALID_FILE",
    "message": "The uploaded CSV is missing the description column."
  }
}
```
