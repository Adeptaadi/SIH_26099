from fastapi import APIRouter

router = APIRouter()

@router.post("/materials/upload")
def upload_materials():
    return {"message": "Not implemented"}
