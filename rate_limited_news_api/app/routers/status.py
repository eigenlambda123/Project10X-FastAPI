# app/routes/status.py
from fastapi import APIRouter
from app.redis_cache import get_scrape_status
from app.rate_limit import limiter

router = APIRouter()

@router.get("/status")
async def get_status():
    """
    Fetches the current status of the scraper and rate limits
    provides information about the scraping status for various sources
    """
    return {
        "scrape_status": {
            "bbc": await get_scrape_status("bbc"),
            "cnn": await get_scrape_status("cnn"),
            "hn": await get_scrape_status("hn")
        },
        "rate_limit_info": {
            "limit": "3/minute (default)",
            "enforced_by": "SlowAPI"
        },
        "cache": {
            "ttl_seconds": 60,
            "backing_store": "Redis"
        }
    }
