from fastapi import APIRouter

router = APIRouter()

@router.get("/notes")
def get_notes():
    return {"notes": []}
