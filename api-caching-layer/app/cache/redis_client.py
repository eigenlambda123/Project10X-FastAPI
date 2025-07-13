import redis
from fastapi import Depends

def get_redis_client():
    return redis.Redis(host="localhost", port=6379, decode_responses=True)