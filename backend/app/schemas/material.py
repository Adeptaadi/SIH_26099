from typing import Optional, Dict, Any
from pydantic import BaseModel

class MaterialBase(BaseModel):
    material_id: str
    organization_id: str
    description: str

class MaterialCreate(MaterialBase):
    normalized_description: Optional[str] = None
    attributes: Optional[Dict[str, Any]] = None

class MaterialOut(MaterialBase):
    id: int
    normalized_description: Optional[str] = None
    attributes_json: Optional[str] = None

    class Config:
        from_attributes = True

class UploadResponse(BaseModel):
    upload_id: str
    organization_id: str
    records_processed: int
    records_rejected: int
    status: str
