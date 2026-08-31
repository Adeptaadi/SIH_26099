from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas.match import MatchingRequest, MatchingResponse, MatchOut
from app.services.matching_service import (
    run_matching_pipeline,
    get_all_matches,
    get_match_by_id
)

router = APIRouter()

@router.post("/matching/run", response_model=MatchingResponse)
def run_matching(
    request: MatchingRequest,
    db: Session = Depends(get_db)
):
    return run_matching_pipeline(
        db=db,
        organization_a=request.organization_a,
        organization_b=request.organization_b
    )

@router.get("/matches", response_model=List[MatchOut])
def list_matches(db: Session = Depends(get_db)):
    return get_all_matches(db=db)

@router.get("/matches/{match_id}", response_model=MatchOut)
def get_match(match_id: str, db: Session = Depends(get_db)):
    match = get_match_by_id(db=db, match_id=match_id)
    if not match:
        raise HTTPException(
            status_code=404,
            detail={
                "error": {
                    "code": "MATCH_NOT_FOUND",
                    "message": f"Match with ID '{match_id}' not found."
                }
            }
        )
    return match
