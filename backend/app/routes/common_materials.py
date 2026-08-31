from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas.common_material import CommonMaterialOut
from app.services.common_material_service import get_all_common_materials

router = APIRouter()

@router.get("/common-materials", response_model=List[CommonMaterialOut])
def list_common_materials(db: Session = Depends(get_db)):
    return get_all_common_materials(db=db)
