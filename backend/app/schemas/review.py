from pydantic import BaseModel, Field

class ReviewRequest(BaseModel):
    decision: str = Field(..., pattern="^(APPROVED|REJECTED)$")

class ReviewOut(BaseModel):
    match_id: str
    decision: str
    status: str

    class Config:
        from_attributes = True
