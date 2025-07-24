# About Dockerized Production API

A modular, container-ready API built with **FastAPI** and **Docker**, designed to demonstrate a realistic microservice setup with:

- **Dockerfile** and **Docker Compose** for containerized environments
- **Environment-based config** via `.env` and Pydantic settings
- **Logging middleware** and observability endpoints
- **Async SQLModel** with SQLite
- Clean code structure for deployment readiness

This project includes a basic `Item` model with CRUD endpoints, uses pagination, and exposes `/health` and (optionally) `/metrics` endpoints. It is optimized to run **entirely within Docker**.

---

## Route Documentation

---

### **GET /items/**

**Description:** Returns a paginated list of items from the database.

**Query Parameters:**

|Name|Type|Default|Description|
|---|---|---|---|
|limit|int|10|Number of results to return|
|offset|int|0|Number of items to skip|

**Response Example:**

```json
[
  {
    "id": 1,
    "title": "Sample Item",
    "description": "This is a test item.",
    "created_at": "2024-07-22T10:12:00"
  }
]
```

---

### **GET /items/{id}**

**Description:** Returns details of a single item by ID.

**Response Example:**

```json
{
  "id": 1,
  "title": "Sample Item",
  "description": "This is a test item.",
  "created_at": "2024-07-22T10:12:00"
}
```

---

### **POST /items/**

**Description:** Creates a new item in the database.

**Request Body:**

```json
{
  "title": "New Item",
  "description": "Something new."
}
```

**Response Example:**

```json
{
  "id": 2,
  "title": "New Item",
  "description": "Something new.",
  "created_at": "2024-07-22T10:15:00"
}
```

---

### **GET /health/**

**Description:** Simple health check endpoint to verify if container/app is up.

**Response:**

```json
{
  "status": "ok"
}
```

---

## Docker Setup

This API is **fully containerized** using Docker and Docker Compose.

### **Dockerfile:**

- Based on `python:3.11-slim`
- Installs dependencies from `requirements.txt`
- Sets environment to production
- Runs Uvicorn with multiple workers:

```bash
uvicorn main:app --host 0.0.0.0 --port 80 --workers 4 --proxy-headers
```

### **docker-compose.yml:**

- Runs FastAPI app container
- Optionally includes Redis or database service
- Supports `.env` config override

```yaml
services:
  app:
    build: .
    ports:
      - "8000:80"
    env_file:
      - .env
```

### **.dockerignore**

Includes:

```txt
__pycache__
.env
*.sqlite
```

---

## Features

|Feature|Description|
|---|---|
|**Dockerized API**|Fully containerized with Dockerfile + Compose|
|**Async ORM**|Built with SQLModel and async SQLite|
|**Structured Logging**|Logs request/response to STDOUT for production containers|
|**Observability**|Health endpoint; optional `/metrics` and log support|
|**Environment Config**|Uses `.env` for secure and dynamic settings|

---

## Project Structure

```text
app/
├── core/
│   └── config.py            # Environment configs
├── models/
│   └── item.py              # SQLModel schema for Item
├── schemas/
│   └── item.py              # Pydantic schemas
├── routers/
│   └── items.py             # /items routes
├── db.py                    # AsyncSession + init logic
├── logging_middleware.py    # Request/response logging
├── main.py                  # FastAPI app setup
Dockerfile
.dockerignore
.env.example
docker-compose.yml
README.md
```

---

## Usage

```bash
# Build image
$ docker-compose build

# Run app (with .env file)
$ docker-compose up

# App will be available at:
http://localhost:8000/items/
```

---

## Notes

- Optimized for **local development** and **production parity**
- Docker Compose can be extended to include Redis, Postgres, or Nginx proxy
- All logs go to **stdout** — compatible with container log collectors
