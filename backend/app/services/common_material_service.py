import json
from typing import List
from sqlalchemy.orm import Session
from app.db.models import CommonMaterialModel
from app.schemas.common_material import CommonMaterialOut, SourceMaterial

def get_all_common_materials(db: Session) -> List[CommonMaterialOut]:
    cms = db.query(CommonMaterialModel).order_by(CommonMaterialModel.created_at.desc()).all()
    results = []

    for cm in cms:
        sources_raw = json.loads(cm.source_materials_json) if cm.source_materials_json else []
        sources = [
            SourceMaterial(
                organization_id=s.get("organization_id", ""),
                material_id=s.get("material_id", ""),
                description=s.get("description")
            )
            for s in sources_raw
        ]

        attrs = json.loads(cm.attributes_json) if cm.attributes_json else None
        # Handle if attrs is a list of attribute names vs dict
        attrs_dict = {"matched_attributes": attrs} if isinstance(attrs, list) else attrs

        results.append(
            CommonMaterialOut(
                common_material_id=cm.common_material_id,
                canonical_description=cm.canonical_description,
                attributes=attrs_dict,
                source_materials=sources
            )
        )

    return results
