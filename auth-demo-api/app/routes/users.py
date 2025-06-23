from fastapi import APIRouter

router = APIRouter()

@router.post("/")
async def create_user():
    return {"message": "User creation placeholder"}