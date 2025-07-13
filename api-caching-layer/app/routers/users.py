from fastapi import APIRouter, Depends, Request
from app.cache.redis_client import get_redis_client
from app.cache.utils import invalidate_cache
from app.cache.decorator import cache_response

router = APIRouter()

@router.get("/users/{user_id}")
@cache_response(ttl=120) # use custom cache decorator with a TTL of 120 seconds
async def get_user(user_id: int, request: Request, redis = Depends(get_redis_client)):
    """
    GET user details and cache the response
    """
    return {"user_id": user_id, "name": "Cached User"}