from typing import List, Optional, Dict, Any
from pydantic import BaseModel

class MatchingRequest(BaseModel):
    organization_a: str
    organization_b: str

class MatchingResponse(BaseModel):
    job_id: str
    status: str
    matches_found: int

class ScoreBreakdown(BaseModel):
    semantic: float = 0.0
    attribute: float = 0.0
    specification: float = 0.0

class MatchOut(BaseModel):
    match_id: str
    material_a_id: str
    material_b_id: str
    material_a: Optional[Dict[str, Any]] = None
    material_b: Optional[Dict[str, Any]] = None
    classification: str
    confidence: float
    scores: ScoreBreakdown
    matched_attributes: List[str] = []
    differences: List[Any] = []
    explanation: Optional[str] = None
    status: str

    class Config:
        from_attributes = True
