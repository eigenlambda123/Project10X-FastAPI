import redis.asyncio as redis
import json

# Connect to local Redis
redis_client = redis.Redis(
    host="localhost",
    port=6379,
    db=0,
    decode_responses=True  # Automatically decode from bytes to str
)

CACHE_TTL_SECONDS = 60  # Customize TTL as needed

async def get_cache(key: str):
    data = await redis_client.get(key)
    if data:
        return json.loads(data)
    return None

async def set_cache(key: str, value, ttl: int = CACHE_TTL_SECONDS):
    await redis_client.set(key, json.dumps(value), ex=ttl)


async def set_scrape_status(source: str, status: str):
    await redis_client.set(f"status:{source}", status, ex=300)

async def get_scrape_status(source: str):
    return await redis_client.get(f"status:{source}")