from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.services.evaluation_service import (
    compute_evaluation_metrics,
    get_ablation_metrics,
    get_hard_negative_demos
)

router = APIRouter()

@router.get("/evaluation/metrics")
def get_metrics(db: Session = Depends(get_db)):
    return compute_evaluation_metrics(db=db)

@router.get("/evaluation/ablation")
def get_ablation(db: Session = Depends(get_db)):
    return get_ablation_metrics(db=db)

@router.get("/demo/hard-negatives")
def get_hard_negatives(db: Session = Depends(get_db)):
    return get_hard_negative_demos(db=db)
