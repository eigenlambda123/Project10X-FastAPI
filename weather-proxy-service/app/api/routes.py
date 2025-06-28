from fastapi import APIRouter

router = APIRouter()

@router.get("/weather")
async def get_weather():
    return {"message": "Weather route ready."}