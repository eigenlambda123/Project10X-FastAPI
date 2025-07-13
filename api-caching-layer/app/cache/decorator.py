import json
from functools import wraps
from fastapi import Request
from app.cache.redis_client import get_redis_client
from app.cache.metrics import record_hit, record_miss

def cache_response(ttl: int = 60):
    """
    Custom decorator to cache API responses in Redis
    - ttl: Time to live for the cache in seconds.
    - If 'nocache' query parameter is set to true, it skips caching.
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Extract the request object from args or kwargs
            request: Request = kwargs.get("request") or args[0]
            # Get query parameters as a dict
            query_params = dict(request.query_params)
            # Check if 'nocache' query param is set to true to skip cache
            skip_cache = query_params.get("nocache", "false").lower() == "true"

            # Generate a cache key using HTTP method and URL path
            cache_key = f"{request.method}:{request.url.path}"
            redis = get_redis_client()

            # If not skipping cache, try to fetch from Redis
            if not skip_cache:
                cached = redis.get(cache_key)
                if cached:
                    # Cache hit: record and return cached response
                    record_hit(cache_key)
                    return json.loads(cached)
                else:
                    # Cache miss: record miss
                    record_miss(cache_key)

            # Call the actual endpoint function
            response = await func(*args, **kwargs)

            # Store response in cache if it's a dict and not skipping cache
            if not skip_cache and isinstance(response, dict):
                redis.set(cache_key, json.dumps(response), ex=ttl)

            # Return the response (from cache or fresh)
            return response
        return wrapper
    return decorator