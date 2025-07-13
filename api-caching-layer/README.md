# About API Caching Layer

A modular caching layer built with **FastAPI** and **Redis**.
This project demonstrates best practices in **caching responses**, **dependency injection**, **cache invalidation**, and **observability via metrics**.
It showcases how to integrate Redis into an async API architecture for performance optimization and real-world scalability features.

---

## Route Documentation

This API provides basic endpoints for managing users and posts, with **GET routes cached via Redis**.
It also includes admin routes to **manually invalidate cached entries** and to **inspect cache performance metrics**.

---

### **GET /api/users/{id}**

**Description:** Get a single user by ID. Response is cached in Redis for 120 seconds.

**Response:**

```json
{
  "user": {
    "id": 1,
    "name": "Cached User A"
  }
}
```

---

### **PUT /api/users/{id}**

**Description:** Update a user by ID. Invalidates the cached `GET /users/{id}` response.

**Request Body:**

```json
{
  "name": "Updated User A"
}
```

**Response:**

```json
{
  "message": "User updated"
}
```

---

### **GET /api/posts/**

**Description:** Get a list of posts. Response is cached for 90 seconds.

**Query Parameters:**

| Name    | Type | Default | Description                                    |
| ------- | ---- | ------- | ---------------------------------------------- |
| nocache | bool | false   | Set to `true` to bypass cache for this request |

**Response:**

```json
{
  "posts": ["Cached post A", "Cached post B"]
}
```

---

### **POST /api/posts/**

**Description:** Create a new post. Automatically invalidates the `GET /posts/` cache.

**Request Body:**

```json
{
  "title": "New Post A"
}
```

**Response:**

```json
{
  "message": "Post created"
}
```

---

### **DELETE /api/invalidate/{key}**

**Description:** Manually invalidate any cache entry by its exact key (e.g. `GET:/api/posts/`).

**Response:**

```json
{
  "message": "Cache key deleted"
}
```

---

### **GET /metrics/cache**

**Description:** View cache hit/miss metrics and usage statistics.

**Response:**

```json
{
  "hits": 5,
  "misses": 2,
  "top_keys": [["GET:/api/posts/", 7]],
  "total_cached_keys": 1
}
```

---

## Features

| Feature             | Description                                                        |
| ------------------- | ------------------------------------------------------------------ |
| Redis Integration   | Stores GET responses in Redis with TTL support                     |
| Cache Decorator     | Reusable `@cache_response(ttl)` decorator for FastAPI              |
| TTL Expiry          | Each cached response expires automatically after a fixed duration  |
| Manual Invalidation | Clear cache by key using an admin DELETE route                     |
| Auto Invalidate     | Writes (POST/PUT) auto-invalidate related GET cache                |
| Conditional Caching | Skips cache if response is not 200 or if `?nocache=true` is passed |
| Metrics Route       | Track hits, misses, top keys, and total Redis keys                 |

---

## Models

* `User`: Simulated user object with ID and name
* `Post`: Simulated post object with title
* Uses plain dictionaries as return types — no persistent DB layer in this project
* Caching and metrics logic are layered around these basic simulated responses

---

## Project Structure

```text
app/
├── main.py                # FastAPI app + route registration
├── routers/
│   ├── users.py           # /users routes (GET, PUT)
│   ├── posts.py           # /posts routes (GET, POST)
│   └── metrics.py         # /metrics/cache
├── cache/
│   ├── decorator.py       # @cache_response logic
│   ├── utils.py           # invalidate_cache helper
│   ├── metrics.py         # hit/miss tracking
│   └── redis_client.py    # get_redis_client()
├── core/
│   └── config.py          # (if environment configs are needed)
```

---

## Notes

* The Redis cache key format is: `GET:/api/posts/`, based on method + route
* TTL is configurable per endpoint via the decorator
* Metrics are stored in-memory and reset on app restart
* The cache decorator supports `nocache=true` to force bypass
* Ideal for plugging into real apps with DB-backed models and user-specific cache keys

---

Let me know if you'd like a badge-style summary, add real DB logic later, or cross-link this to other Project10X projects.
