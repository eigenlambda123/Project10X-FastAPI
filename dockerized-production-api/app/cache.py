import redis.asyncio as redis
from app.core.config import Settings

settings = Settings()

# Create a Redis client using the settings
redis_client = redis.from_url(settings.REDIS_URL, decode_responses=True)
