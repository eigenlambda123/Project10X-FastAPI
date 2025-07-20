# About Rate-Limited News API

A modular news aggregation API built with **FastAPI**, featuring:

* **Web scraping** via `httpx.AsyncClient` + `BeautifulSoup`
* **Caching** scraped responses in **Redis**
* **Rate limiting** with `SlowAPI`
* **Proxy rotation**, **logging**, and **scraper health status**
* Designed for extensibility, resilience, and real-world deployment readiness

This project pulls articles from sources like **CNN**, **BBC**, and **Hacker News**, unifies them into a common schema, and exposes them through a simple `/news/` endpoint.

---

## Route Documentation

---

### **GET /news/**

**Description:** Return the latest normalized headlines from supported sources.
Responses are **cached in Redis per source** for a configurable TTL (default: 300s).
Includes optional proxy rotation to reduce blocking.

**Query Parameters:**

| Name    | Type | Default | Description                     |
| ------- | ---- | ------- | ------------------------------- |
| source  | str  | all     | Filter by source (cnn, hn, etc) |
| nocache | bool | false   | Force bypass of Redis cache     |

**Response (example):**

```json
[
  {
    "title": "My Ultimate Self-Hosting Setup",
    "url": "https://codecaptured.com/blog/my-ultimate-self-hosting-setup/",
    "source": "hn"
  },
  {
    "title": "Global Stocks Rally Amid Inflation Dip",
    "url": "https://cnn.com/article-xyz",
    "source": "cnn"
  }
]
```

---

### **GET /status/**

**Description:** Returns internal system health info including:

* Last scrape time per source
* Scraper error states (if any)
* Redis connection status
* Rate limiting config state

**Response:**

```json
{
  "redis": "connected",
  "scrapers": {
    "hn": "ok",
    "cnn": "null",
    "bbc": "error"
  },
  "rate_limit": {
    "limit": "20/minute",
    "active": true
  }
}
```

---

## Features

| Feature             | Description                                                          |
| ------------------- | -------------------------------------------------------------------- |
| **Async Scraping**  | Each source uses an `httpx.AsyncClient` with timeout + retries       |
| **Proxy Rotation**  | Rotates headers and proxies per request for resilience               |
| **Redis Caching**   | Cache entire JSON responses using hashed request key                 |
| **Status Tracking** | Scrape status is tracked in Redis (e.g., `null`, `ok`, `error`) |
| **Logging**         | Scrape attempts are logged: source, success/fail, and response time  |
| **Rate Limiting**   | Requests are throttled via IP or user limits using SlowAPI           |


---

## Project Structure

```text
app/
├── core/
│   └── config.py            # Environment configs and settings
├── routers/
│   ├── news.py              # /news route: async scraping and response normalization
│   ├── status.py            # /status route: scrape status tracker
│   ├── logger.py            # Logging logic for all scrapes
│   ├── rate_limit.py        # SlowAPI middleware setup
│   ├── redis_cache.py       # Redis client + get/set helpers
│   └── scraper.py           # Per-source scraper logic using httpx + BeautifulSoup
├── main.py                  # FastAPI app setup and route includes
.env
README.md
requirements.txt
```

---

## Supported Sources

| Source | Description                | Cache Key  | Scrape Status Key   |
| ------ | -------------------------- | ---------- | ------------------- |
| `hn`   | Hacker News (top articles) | `news:hn`  | `scrape:status:hn`  |
| `cnn`  | CNN (top stories page)     | `news:cnn` | `scrape:status:cnn` |
| `bbc`  | BBC (front page)           | `news:bbc` | `scrape:status:bbc` |

---

## Implementation Highlights

* **Redis Cache Keys**: `news:<source>` (e.g., `news:hn`, `news:cnn`)
* **Scrape Status Keys**: `scrape:status:<source>`
* **Proxy Rotation**: Chooses a random User-Agent and/or proxy for each scrape request
* **Error Logging**: If a scraper fails, its status is set to `"error"` in Redis
* **Try/Except Handling**: Each scraper wraps logic with:

```python
except Exception as e:
    await set_scrape_status("hn", "error")
```

---

## How to Extend

To add a new news source:

1. Create a new scraper function in `services/scraper_registry.py`
2. Register it with the existing scraper mapping
3. Define:

   * How to fetch the page (e.g., with `httpx`)
   * How to parse the DOM with `BeautifulSoup`
   * How to return a `List[NewsItem]`

---

## Notes

* All scrapers are **async** and run independently.
* Redis is required to store cache and scrape status (local or Docker OK).
* Cache TTLs are adjustable per source or globally.
* If a scraper fails, it will **not affect** others — fallback to cached result if available.
* Status endpoint is a **non-authenticated** debug feature for now.
