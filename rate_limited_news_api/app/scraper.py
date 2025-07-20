import httpx
import asyncio
from bs4 import BeautifulSoup
from typing import List, Dict
from app.redis_cache import get_cache, set_cache
from app.logger import logger
import time

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/114.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 Version/14.0.3 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/109.0.0.0 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 Version/15.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0"
]


async def fetch_html(url: str) -> str | None:
    """
    Fetches HTML content from a given URL asynchronously
    """
    try:
        # Use the configured timeout and headers
        async with httpx.AsyncClient(timeout=10.0, headers=HEADERS) as client:
            response = await client.get(url)
            response.raise_for_status()
            return response.text
    except httpx.HTTPError:
        return None
    


async def fetch_bbc_news() -> List[Dict]:
    """
    Fetches the latest news articles from BBC News and scrapes the HTML content
    """
    # caching
    cache_key = "news:bbc"
    cached = await get_cache(cache_key)
    if cached:
        logger.info(f"Cache hit for {cache_key}")
        return cached
    logger.info(f"Cache miss for {cache_key}. Scraping BBC News...")
    start = time.time()

    try:
        html = await fetch_html("https://www.bbc.com/news")
        if not html:
            logger.warning("Empty or failed HTML fetch for BBC")
            return []

        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(html, "html.parser")
        articles = []

        # Select news articles from the BBC News page
        # Adjust the selector based on the actual structure of the page
        # This example assumes articles are linked with a specific data-testid attribute
        for item in soup.select("a[data-testid='internal-link']"):

            # Extract the title and URL from each article item
            title = item.get_text(strip=True)
            url = item["href"]
            full_url = f"https://www.bbc.com{url}" if url.startswith("/") else url

            # Append the article details to the list
            articles.append({
                "source": "bbc",
                "title": title,
                "url": full_url,
                "published_at": None
            })

        # cache, log, and return
        articles = articles[:10]
        await set_cache(cache_key, articles)
        logger.info(f"Scraped BBC ({len(articles)} articles) in {time.time() - start:.2f}s")
        return articles

    except Exception as e:
        logger.error(f"Error scraping BBC: {e}")
        return []



async def fetch_cnn_news() -> List[Dict]:
    """
    Fetches the latest news articles from CNN and scrapes the HTML content
    """
    # caching
    cache_key = "news:cnn"
    cached = await get_cache(cache_key)
    if cached:
        logger.info(f"Cache hit for {cache_key}")
        return cached
    logger.info(f"Cache miss for {cache_key}. Scraping CNN News...")
    start = time.time()
    
    try:
        html = await fetch_html("https://edition.cnn.com/world")
        if not html:
            logger.warning("Empty or failed HTML fetch for CNN")
            return []

        soup = BeautifulSoup(html, "html.parser")
        articles = []

        # Select news articles from the CNN World page
        # uses a selector that matches CNN's article links
        for item in soup.select("a[data-link-type='article']"):
            title = item.get_text(strip=True)
            url = item["href"]
            full_url = f"https://edition.cnn.com{url}" if url.startswith("/") else url
            articles.append({
                "source": "cnn",
                "title": title,
                "url": full_url,
                "published_at": None
            })

        # cache, log, and return
        articles = articles[:10]
        await set_cache(cache_key, articles)
        logger.info(f"Scraped CNN ({len(articles)} articles) in {time.time() - start:.2f}s")
        return articles

    except Exception as e:
        logger.error(f"Error scraping CNN: {e}")
        return []



async def fetch_hn_news() -> List[Dict]:
    """
    Fetches the latest news articles from Hacker News and scrapes the HTML content
    """
    # caching
    cache_key = "news:hn"
    cached = await get_cache(cache_key)
    if cached:
        logger.info(f"Cache hit for {cache_key}")
        return cached
    
    logger.info(f"Cache miss for {cache_key}. Scraping Hacker News...")
    start = time.time()
    
    try:
        html = await fetch_html("https://news.ycombinator.com/")
        if not html:
            logger.warning("Empty or failed HTML fetch for Hacker News")
            return []

        soup = BeautifulSoup(html, "html.parser")
        articles = []

        # Select news articles from the Hacker News page
        # This assumes articles are listed in <tr> elements with class "athing"
        for row in soup.select("tr.athing"):
            title_tag = row.select_one("span.titleline a") # This selects the title link
            if not title_tag:
                continue
            
            # Extract the title and URL from each article item
            # The title is in the <a> tag with class "titlelink"
            title = title_tag.get_text(strip=True)
            url = title_tag.get("href")
            if not url:
                continue


            articles.append({
                "source": "hackernews",
                "title": title,
                "url": url,
                "published_at": None  # HN does not give this directly
            })

        # cache and return
        articles = articles[:10]
        await set_cache(cache_key, articles)
        logger.info(f"Scraped Hacker News ({len(articles)} articles) in {time.time() - start:.2f}s")
        return articles
    
    except Exception as e:
        logger.error(f"Error scraping HN: {e}")
        return []




async def get_all_news() -> List[Dict]:
    """
    Fetches news articles from multiple sources asynchronously
    """
    results = await asyncio.gather(
        fetch_bbc_news(),
        fetch_cnn_news(),
        fetch_hn_news()
    )
    all_articles = []
    for site_articles in results:
        all_articles.extend(site_articles)
    return all_articles



# source-specific fetch functions
SCRAPER_MAP = {
    "bbc": fetch_bbc_news,
    "cnn": fetch_cnn_news,
    "hackernews": fetch_hn_news,
}

async def get_news_by_source(source: str) -> List[Dict]:
    """
    Fetches news articles from a specific source based on the provided source name.
    """
    fetcher = SCRAPER_MAP.get(source.lower())
    if not fetcher:
        return []
    return await fetcher()


def paginate(data: List[Dict], limit: int = 10, page: int = 1) -> List[Dict]:
    """
    Paginates the given data
    """
    start = (page - 1) * limit
    end = start + limit
    return data[start:end]