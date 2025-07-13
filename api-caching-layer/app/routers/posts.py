from fastapi import APIRouter, Depends, Request
from app.cache.redis_client import get_redis_client
from app.cache.decorator import cache_response

router = APIRouter()

@router.get("/posts/")
@cache_response(ttl=90) # use custom cache decorator with a TTL of 90 seconds
async def get_posts(request: Request, redis = Depends(get_redis_client)):
    """
    GET posts and cache the response
    """
    return {"posts": ["Cached post A", "Cached post B"]}
