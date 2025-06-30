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
