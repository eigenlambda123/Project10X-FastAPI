# Project10X: The FastAPI Builder Series

A structured, hands-on journey through 10 backend projects, designed to progressively build and deepen API development skills using **FastAPI**, asynchronous programming, and modern Python backend tooling.

---

## Overview

This repository documents a curated sequence of FastAPI projects developed to explore asynchronous web API design in a practical, incremental way.

Each project focuses on production-style backend architecture, and includes:

* Core CRUD and RESTful logic
* FastAPI testing with `TestClient` and `pytest`
* Clean use of Pydantic models and validation
* Optional stretch goals for async integrations, caching, or external API use

Projects are structured to reflect real-world systems rather than isolated examples, with an emphasis on clean code, modular design, and deep mastery of FastAPI’s async capabilities.

---

## Projects Included

| #  | Project Name                          | Key Features                                                  | Stack                    |
| -- | ------------------------------------- | ------------------------------------------------------------- | ------------------------ |
| 1  | Mini Notes API                        | CRUD, body/query params, response models                      | FastAPI + Pydantic       |
| 2  | Book Review API                       | Nested models, rating system, filtering reviews               | FastAPI + Pydantic       |
| 3  | Auth Demo API                         | JWT authentication, role checking, reusable dependencies      | FastAPI + OAuth2/JWT     |
| 4  | Background Tasks Service              | Email simulation, async task execution                        | FastAPI + BackgroundTasks|
| 5  | Weather Proxy Microservice            | Async fetch, external API call, response transformation       | FastAPI + httpx          |
| 6  | Async Blog API                        | Async DB with SQLModel, pagination, tag-based filtering       | FastAPI + SQLModel       |
| 7  | API Caching Layer                     | In-memory or Redis-based caching for performance              | FastAPI + Redis (optional)|
| 8  | Task Queue Worker API                 | Background job queue with Celery + Redis                     | FastAPI + Celery         |
| 9  | Rate-Limited News API                 | Async scraping, throttling, client headers                    | FastAPI + httpx + limits |
| 10 | Dockerized Production API             | Full Docker setup, env configs, async logging                 | FastAPI + Uvicorn + Docker|

Each project resides in its own folder with documentation for setup, features, and testing.

---

## Skills and Technologies

* Python 3.12+
* FastAPI (Async Web Framework)
* Pydantic for validation and serialization
* JWT Authentication & OAuth2 flows
* SQLModel (async DB ORM)
* PostgreSQL / SQLite
* `httpx` for async external API calls
* Redis and Celery (for background jobs and caching)
* Docker & Uvicorn for production setup
* Testing with `pytest`, `TestClient`, and `httpx.AsyncClient`
* RESTful API Design and OpenAPI documentation
* Git and Modular Project Architecture

---

## Purpose

**Project10X: The FastAPI Builder Series** is designed as a deep learning track for mastering asynchronous API development in Python using FastAPI. It reflects a commitment to:

* Understanding async I/O and API design at a production level
* Testing and documenting APIs with clarity and completeness
* Applying FastAPI's full feature set: background tasks, external APIs, auth, caching, and deployment

---

## Usage

Each project includes:

* Clear setup instructions and dependency requirements
* A list of core features and optional stretch goals
* Backend tests for routes and logic
* Examples of query, path, and body parameter usage
* Tools for async workflows and real-world API use cases

This repo is open for exploration, learning, and contribution. Forks, pull requests, and suggestions are welcome.

---

## License

This repository is open source under the MIT License.

---

*Created and maintained by RM Villa.*