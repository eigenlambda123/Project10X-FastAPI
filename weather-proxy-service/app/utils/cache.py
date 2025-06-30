import time
from typing import Any, Tuple

CACHE_TTL_SECONDS = 600  # 10 minutes

# Structure: { key: (expires_at_timestamp, data) }
cache_store: dict[str, Tuple[float, Any]] = {} 



def make_cache_key(city: str = "", lat: float = None, lon: float = None) -> str:
    """Generate a cache key based on city name or coordinates"""
    if city:
        return f"city:{city.lower()}"
    elif lat is not None and lon is not None:
        return f"coords:{lat:.4f},{lon:.4f}"
    return "invalid"


def get_from_cache(key: str):
    """Retrieve data from cache by key"""
    # get the entry from the cache
    entry = cache_store.get(key) 

    # if the entry does not exist or has expired, return None
    if not entry:
        return None
    
    # check if the entry has expired
    expires_at, data = entry

    # If the current time is greater than the expiration time, remove it and return None
    if time.time() > expires_at:
        # remove the expired entry from the cache
        del cache_store[key]  
        return None
    return data
