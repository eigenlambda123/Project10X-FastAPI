from fastapi import APIRouter, Request, Query, HTTPException, status
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address
from app.rate_limit import limiter
from app.scraper import get_all_news, get_news_by_source, paginate

router = APIRouter(prefix="/news")


@router.get("/")
@limiter.limit("3/minute") # Limit to 3 requests per minute
async def news_endpoint(request: Request):
    return await get_all_news()




@router.get("/with_pagination")
@limiter.limit("3/minute")
async def all_news(
    request: Request,
    limit: int = Query(10, ge=1),
    page: int = Query(1, ge=1)
):
    """
    Fetches all news articles with pagination
    """
    try:
        data = await get_all_news()
        paginated = paginate(data, limit, page)
        return {"total": len(data), "page": page, "limit": limit, "results": paginated}
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to fetch news")
    


@router.get("/{source}")
@limiter.limit("3/minute")
async def news_by_source(
    source: str,
    request: Request,
    limit: int = Query(10, ge=1),
    page: int = Query(1, ge=1)
):
    """
    Fetches news articles from a specific source with pagination
    """
    try:
        data = await get_news_by_source(source)
        if not data:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No news found for '{source}'")
        paginated = paginate(data, limit, page)
        return {"total": len(data), "page": page, "limit": limit, "results": paginated}
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to fetch news")