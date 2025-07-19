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
    """
    Fetches the latest news articles from BBC News and scrapes the HTML content
    """
    html = await fetch_html("https://www.bbc.com/news")
    if not html:
        print("BBC HTML fetch failed or returned empty!")
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
    # Return the first 10 articles
    return articles[:10]



async def fetch_cnn_news() -> List[Dict]:
    """
    Fetches the latest news articles from CNN and scrapes the HTML content
    """
    html = await fetch_html("https://edition.cnn.com/world")
    if not html:
        print("CNN HTML fetch failed or returned empty!")
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

    return articles[:10]



async def get_all_news() -> List[Dict]:
    """
    Fetches news articles from multiple sources asynchronously
    """
    results = await asyncio.gather(
        fetch_bbc_news(),
        fetch_cnn_news()
    )
    all_articles = []
    for site_articles in results:
        all_articles.extend(site_articles)
    return all_articles