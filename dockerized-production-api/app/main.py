from fastapi import FastAPI
from app.db import create_db_and_tables
from app.core.config import settings

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
