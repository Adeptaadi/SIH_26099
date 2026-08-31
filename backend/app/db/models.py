from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, Text, DateTime
from app.db.database import Base

class MaterialModel(Base):
    __tablename__ = "materials"

    id = Column(Integer, primary_key=True, index=True)
    material_id = Column(String, index=True)
    organization_id = Column(String, index=True)
    description = Column(Text, nullable=False)
    normalized_description = Column(Text, nullable=True)
    attributes_json = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class MatchModel(Base):
    __tablename__ = "matches"

    id = Column(Integer, primary_key=True, index=True)
    match_id = Column(String, unique=True, index=True)
    material_a_id = Column(String, index=True)
    material_b_id = Column(String, index=True)
    classification = Column(String, nullable=False) # EQUIVALENT, REVIEW, DIFFERENT
    confidence = Column(Float, default=0.0)
    semantic_score = Column(Float, default=0.0)
    attribute_score = Column(Float, default=0.0)
    specification_score = Column(Float, default=0.0)
    matched_attributes_json = Column(Text, nullable=True) # JSON list
    differences_json = Column(Text, nullable=True) # JSON list
    explanation = Column(Text, nullable=True)
    status = Column(String, default="PENDING_REVIEW") # PENDING_REVIEW, APPROVED, REJECTED
    created_at = Column(DateTime, default=datetime.utcnow)

class ReviewModel(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    match_id = Column(String, index=True)
    decision = Column(String, nullable=False) # APPROVED, REJECTED
    reviewed_at = Column(DateTime, default=datetime.utcnow)

class CommonMaterialModel(Base):
    __tablename__ = "common_materials"

    id = Column(Integer, primary_key=True, index=True)
    common_material_id = Column(String, unique=True, index=True)
    canonical_description = Column(Text, nullable=False)
    attributes_json = Column(Text, nullable=True) # JSON object
    source_materials_json = Column(Text, nullable=True) # JSON list of source records
    created_at = Column(DateTime, default=datetime.utcnow)
