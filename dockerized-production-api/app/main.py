from fastapi import FastAPI
from app.db import create_db_and_tables
from app.core.config import settings
from app.routers import items, metrics

app = FastAPI(title="Dockerized Production API")

@app.on_event("startup")
async def on_startup():
    """
    Create database tables at startup
    """
    await create_db_and_tables()

@app.get("/health")
async def health_check():
    return {"status": "ok"}

app.include_router(items.router)
app.include_router(metrics.router)