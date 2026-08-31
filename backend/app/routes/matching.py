from fastapi import APIRouter

router = APIRouter()

@router.post("/matching/run")
def run_matching():
    return {"message": "Not implemented"}
