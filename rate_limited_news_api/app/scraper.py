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
    

