import redis.asyncio as redis
from app.core.config import settings

# Initialize Redis client using the URL from settings
redis_client = redis.from_url(settings.REDIS_URL, decode_responses=True)
