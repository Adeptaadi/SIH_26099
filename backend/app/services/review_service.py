import json
import uuid
from datetime import datetime
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.db.models import MatchModel, ReviewModel, CommonMaterialModel, MaterialModel
from app.schemas.review import ReviewRequest, ReviewOut

def process_match_review(db: Session, match_id: str, request: ReviewRequest) -> ReviewOut:
    match = db.query(MatchModel).filter(MatchModel.match_id == match_id).first()
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

    decision = request.decision
    match.status = decision

    # Record review entry
    review_entry = ReviewModel(
        match_id=match_id,
        decision=decision,
        reviewed_at=datetime.utcnow()
    )
    db.add(review_entry)

    # If APPROVED, create CommonMaterial record if not already created
    if decision == "APPROVED":
        # Check if common material already exists for these source materials
        existing_cm = db.query(CommonMaterialModel).filter(
            CommonMaterialModel.source_materials_json.contains(match.material_a_id)
        ).first()

        if not existing_cm:
            mat_a = db.query(MaterialModel).filter(MaterialModel.material_id == match.material_a_id).first()
            mat_b = db.query(MaterialModel).filter(MaterialModel.material_id == match.material_b_id).first()

            org_a = mat_a.organization_id if mat_a else "ORG_A"
            org_b = mat_b.organization_id if mat_b else "ORG_B"

            # Canonical description strategy: pick longer/more complete normalized description or mat_b description
            canonical_desc = mat_a.description if mat_a else (mat_b.description if mat_b else "HARMONIZED MATERIAL")
            if mat_b and len(mat_b.description) > len(canonical_desc):
                canonical_desc = mat_b.description

            sources = [
                {"organization_id": org_a, "material_id": match.material_a_id, "description": mat_a.description if mat_a else None},
                {"organization_id": org_b, "material_id": match.material_b_id, "description": mat_b.description if mat_b else None}
            ]

            cm_id = f"CM_{uuid.uuid4().hex[:6].upper()}"
            new_cm = CommonMaterialModel(
                common_material_id=cm_id,
                canonical_description=canonical_desc,
                attributes_json=match.matched_attributes_json,
                source_materials_json=json.dumps(sources)
            )
            db.add(new_cm)

    db.commit()

    return ReviewOut(
        match_id=match_id,
        decision=decision,
        status=match.status
    )
