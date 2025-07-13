from fastapi import APIRouter, Depends
from app.cache.redis_client import get_redis_client

router = APIRouter()

@router.delete("/invalidate/{key}")
def invalidate_cache_key(key: str, redis = Depends(get_redis_client)):
    deleted = redis.delete(key)
    return {"key": key, "deleted": bool(deleted)}
