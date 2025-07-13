import json
from functools import wraps
from fastapi import Depends, Request
from app.cache.redis_client import get_redis_client

def cache_response(ttl: int = 60):
    """
    Decorator to cache the response of a FastAPI endpoint using Redis
    ttl: Time to live for the cache in seconds
    """

    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Extract request and redis client from args or kwargs
            request: Request = kwargs.get("request") or next((arg for arg in args if isinstance(arg, Request)), None)
            redis = kwargs.get("redis") or get_redis_client()

            # Generate a cache key based on the request method and URL path
            cache_key = f"{request.method}:{request.url.path}"

            # Check if the response is cached
            cached = redis.get(cache_key)
            if cached:
                return json.loads(cached)
            
            # Call the original function to get the response
            response = await func(*args, **kwargs)

            # Cache the response
            redis.set(cache_key, json.dumps(response), ex=ttl)

            print(f"[Cache] Checking key: {cache_key}")

            # Log cache hit or miss
            if cached:
                print(f"[Cache] HIT for key: {cache_key}")
            else:
                print(f"[Cache] MISS for key: {cache_key}")

            return response
        return wrapper
    return decorator