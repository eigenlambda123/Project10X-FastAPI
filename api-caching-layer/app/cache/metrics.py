from collections import Counter

cache_stats = {
    "hits": 0,
    "misses": 0,
    "access_log": Counter()  # Tracks key access frequency
}

def record_hit(key: str):
    cache_stats["hits"] += 1
    cache_stats["access_log"][key] += 1

def record_miss(key: str):
    cache_stats["misses"] += 1
    cache_stats["access_log"][key] += 1

def get_metrics():
    top_keys = cache_stats["access_log"].most_common(5)
    return {
        "hits": cache_stats["hits"],
        "misses": cache_stats["misses"],
        "top_keys": top_keys, # Records the top 5 accessed keys
        "total_cached_keys": None
    }
