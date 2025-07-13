from fastapi import APIRouter, Depends
from app.cache.redis_client import get_redis_client

router = APIRouter()

@router.get("/redis-test")
def redis_test(redis = Depends(get_redis_client)):
    redis.set("test_key", "hello")
    return {"cached_value": redis.get("test_key")}