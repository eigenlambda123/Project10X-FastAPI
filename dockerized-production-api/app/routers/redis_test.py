from fastapi import APIRouter
from app.cache import redis_client

router = APIRouter()

@router.get("/cache-test")
async def cache_test():
    """
    Test Redis caching
    """
    await redis_client.set("test_key", "hello")
    value = await redis_client.get("test_key")
    return {"key": "test_key", "value": value}
