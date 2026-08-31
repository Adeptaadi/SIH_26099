from typing import List, Optional
from fastapi import APIRouter, Depends, UploadFile, File, Form, Query
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db.models import MaterialModel
from app.schemas.material import UploadResponse, MaterialOut
from app.services.material_service import process_csv_upload

router = APIRouter()

@router.post("/materials/upload", response_model=UploadResponse)
def upload_materials(
    file: UploadFile = File(...),
    organization_id: str = Form(...),
    db: Session = Depends(get_db)
):
    return process_csv_upload(db=db, file=file, organization_id=organization_id)

@router.get("/materials", response_model=List[MaterialOut])
def get_materials(
    organization_id: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    query = db.query(MaterialModel)
    if organization_id:
        query = query.filter(MaterialModel.organization_id == organization_id)
    return query.all()
