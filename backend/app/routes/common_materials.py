from fastapi import APIRouter

router = APIRouter()

@router.get("/common-materials")
def get_common_materials():
    return {"message": "Not implemented"}
