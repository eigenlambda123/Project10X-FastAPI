import httpx
import asyncio
from bs4 import BeautifulSoup
from typing import List, Dict

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}


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
    html = await fetch_html("https://www.bbc.com/news")
    if not html:
        return []

    soup = BeautifulSoup(html, "html.parser")
    articles = []

    for item in soup.select("a.gs-c-promo-heading"):
        title = item.get_text(strip=True)
        url = item["href"]
        full_url = f"https://www.bbc.com{url}" if url.startswith("/") else url
        articles.append({
            "source": "bbc",
            "title": title,
            "url": full_url,
            "published_at": None
        })

    return articles[:10]