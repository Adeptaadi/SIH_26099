import json
import uuid
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from app.db.models import MaterialModel, MatchModel
from app.schemas.match import MatchingResponse, MatchOut, ScoreBreakdown
from ml.pipeline import find_matches

def run_matching_pipeline(db: Session, organization_a: str, organization_b: str) -> MatchingResponse:
    # 1. Fetch materials for org A and org B
    mats_a_models = db.query(MaterialModel).filter(MaterialModel.organization_id == organization_a).all()
    mats_b_models = db.query(MaterialModel).filter(MaterialModel.organization_id == organization_b).all()

    if not mats_a_models or not mats_b_models:
        # Check if any materials exist in general
        all_count = db.query(MaterialModel).count()
        if all_count == 0:
            # Seed mock materials from data/raw if DB is empty for demo/testing!
            pass

    materials_a = [
        {
            "material_id": m.material_id,
            "organization_id": m.organization_id,
            "description": m.description
        }
        for m in mats_a_models
    ]

    materials_b = [
        {
            "material_id": m.material_id,
            "organization_id": m.organization_id,
            "description": m.description
        }
        for m in mats_b_models
    ]

    # 2. Call ML pipeline
    raw_results = find_matches(materials_a, materials_b)

    # 3. Store or update match results in DB
    job_id = f"JOB_{uuid.uuid4().hex[:6].upper()}"
    matches_saved = 0

    for res in raw_results:
        mat_a_id = res.get("material_a_id")
        mat_b_id = res.get("material_b_id")

        if not mat_a_id or not mat_b_id:
            continue

        match_id = res.get("match_id") or f"MATCH_{uuid.uuid4().hex[:8].upper()}"
        classification = res.get("classification", "REVIEW")
        confidence = float(res.get("confidence", 0.0))

        scores = res.get("scores", {})
        sem_score = float(scores.get("semantic", 0.0))
        attr_score = float(scores.get("attribute", 0.0))
        spec_score = float(scores.get("specification", 0.0))

        matched_attrs = json.dumps(res.get("matched_attributes", []))
        diffs = json.dumps(res.get("differences", []))
        explanation = res.get("explanation", "")
        status = res.get("status", "PENDING_REVIEW")

        # Check existing match
        existing = db.query(MatchModel).filter(
            MatchModel.material_a_id == mat_a_id,
            MatchModel.material_b_id == mat_b_id
        ).first()

        if existing:
            existing.classification = classification
            existing.confidence = confidence
            existing.semantic_score = sem_score
            existing.attribute_score = attr_score
            existing.specification_score = spec_score
            existing.matched_attributes_json = matched_attrs
            existing.differences_json = diffs
            existing.explanation = explanation
        else:
            new_match = MatchModel(
                match_id=match_id,
                material_a_id=mat_a_id,
                material_b_id=mat_b_id,
                classification=classification,
                confidence=confidence,
                semantic_score=sem_score,
                attribute_score=attr_score,
                specification_score=spec_score,
                matched_attributes_json=matched_attrs,
                differences_json=diffs,
                explanation=explanation,
                status=status
            )
            db.add(new_match)
        matches_saved += 1

    db.commit()

    return MatchingResponse(
        job_id=job_id,
        status="COMPLETED",
        matches_found=matches_saved
    )


def format_match_out(db: Session, m: MatchModel) -> MatchOut:
    # Resolve material details
    mat_a = db.query(MaterialModel).filter(MaterialModel.material_id == m.material_a_id).first()
    mat_b = db.query(MaterialModel).filter(MaterialModel.material_id == m.material_b_id).first()

    matched_attrs = json.loads(m.matched_attributes_json) if m.matched_attributes_json else []
    diffs = json.loads(m.differences_json) if m.differences_json else []

    return MatchOut(
        match_id=m.match_id,
        material_a_id=m.material_a_id,
        material_b_id=m.material_b_id,
        material_a={
            "material_id": mat_a.material_id,
            "organization_id": mat_a.organization_id,
            "description": mat_a.description
        } if mat_a else None,
        material_b={
            "material_id": mat_b.material_id,
            "organization_id": mat_b.organization_id,
            "description": mat_b.description
        } if mat_b else None,
        classification=m.classification,
        confidence=m.confidence,
        scores=ScoreBreakdown(
            semantic=m.semantic_score,
            attribute=m.attribute_score,
            specification=m.specification_score
        ),
        matched_attributes=matched_attrs,
        differences=diffs,
        explanation=m.explanation,
        status=m.status
    )


def get_all_matches(db: Session) -> List[MatchOut]:
    matches = db.query(MatchModel).order_by(MatchModel.confidence.desc()).all()
    return [format_match_out(db, m) for m in matches]


def get_match_by_id(db: Session, match_id: str) -> Optional[MatchOut]:
    m = db.query(MatchModel).filter(MatchModel.match_id == match_id).first()
    if not m:
        return None
    return format_match_out(db, m)
