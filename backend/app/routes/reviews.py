from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas.review import ReviewRequest, ReviewOut
from app.services.review_service import process_match_review

router = APIRouter()

@router.post("/matches/{match_id}/review", response_model=ReviewOut)
def review_match(
    match_id: str,
    request: ReviewRequest,
    db: Session = Depends(get_db)
):
    return process_match_review(db=db, match_id=match_id, request=request)
