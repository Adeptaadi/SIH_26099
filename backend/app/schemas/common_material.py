from typing import List, Dict, Any, Optional
from pydantic import BaseModel

class SourceMaterial(BaseModel):
    organization_id: str
    material_id: str
    description: Optional[str] = None

class CommonMaterialOut(BaseModel):
    common_material_id: str
    canonical_description: str
    attributes: Optional[Dict[str, Any]] = None
    source_materials: List[SourceMaterial] = []

    class Config:
        from_attributes = True
