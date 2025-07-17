import asyncio

async def mock_scrape_news():
    await asyncio.sleep(0.5)
    return [{"title": "Test News", "source": "Mock Site"}]