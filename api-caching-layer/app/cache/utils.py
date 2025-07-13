from app.cache.redis_client import get_redis_client

def invalidate_cache(key: str):
    redis = get_redis_client()
    redis.delete(key)
