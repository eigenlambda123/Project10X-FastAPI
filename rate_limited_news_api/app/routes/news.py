from fastapi import APIRouter, Request
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address
from ..rate_limit import limiter
from ..scraper import mock_scrape_news

router = APIRouter(prefix="/news")

@router.get("/")
@limiter.limit("5/minute")
async def get_news(request: Request):
    return {
        "status": "ok",
        "data": await mock_scrape_news()
    }
