from fastapi import APIRouter
from app.cache.metrics import get_metrics
from app.cache.redis_client import get_redis_client

router = APIRouter()

@router.get("/metrics/cache")
def cache_metrics():
    """
    GET cache metrics including total cached keys
    """
    metrics = get_metrics()
    redis = get_redis_client()
    metrics["total_cached_keys"] = len(redis.keys("*"))
    return metrics
