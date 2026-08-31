import io
import json
import uuid
import pandas as pd
from fastapi import UploadFile, HTTPException
from sqlalchemy.orm import Session
from app.db.models import MaterialModel
from app.schemas.material import UploadResponse

def process_csv_upload(db: Session, file: UploadFile, organization_id: str) -> UploadResponse:
    if not file.filename.endswith(".csv"):
        raise HTTPException(
            status_code=400,
            detail={
                "error": {
                    "code": "INVALID_FILE_TYPE",
                    "message": "Only CSV files are accepted."
                }
            }
        )

    try:
        contents = file.file.read()
        df = pd.read_csv(io.BytesIO(contents))
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail={
                "error": {
                    "code": "INVALID_CSV",
                    "message": f"Could not parse CSV file: {str(e)}"
                }
            }
        )

    # Check required columns
    required_cols = {"material_id", "description"}
    missing = required_cols - set(df.columns)
    if missing:
        raise HTTPException(
            status_code=400,
            detail={
                "error": {
                    "code": "MISSING_COLUMNS",
                    "message": f"CSV missing required columns: {', '.join(missing)}"
                }
            }
        )

    records_processed = 0
    records_rejected = 0

    # Process rows
    for index, row in df.iterrows():
        mat_id = str(row.get("material_id", "")).strip()
        desc = str(row.get("description", "")).strip()

        if not mat_id or not desc or mat_id.lower() == "nan" or desc.lower() == "nan":
            records_rejected += 1
            continue

        # Check if already exists for this org
        existing = db.query(MaterialModel).filter(
            MaterialModel.material_id == mat_id,
            MaterialModel.organization_id == organization_id
        ).first()

        if existing:
            # Update existing
            existing.description = desc
        else:
            new_mat = MaterialModel(
                material_id=mat_id,
                organization_id=organization_id,
                description=desc,
                normalized_description=None,
                attributes_json=None
            )
            db.add(new_mat)
        
        records_processed += 1

    db.commit()

    upload_id = f"UP_{uuid.uuid4().hex[:6].upper()}"

    return UploadResponse(
        upload_id=upload_id,
        organization_id=organization_id,
        records_processed=records_processed,
        records_rejected=records_rejected,
        status="SUCCESS"
    )
