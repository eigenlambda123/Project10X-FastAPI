from fastapi import APIRouter, Request
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address
from app.rate_limit import limiter
from app.scraper import get_all_news

router = APIRouter(prefix="/news")


@router.get("/")
async def news_endpoint():
    return await get_all_news()
