from fastapi import APIRouter

router = APIRouter()

@router.post("/matches/{match_id}/review")
def review_match(match_id: str):
    return {"message": "Not implemented"}
