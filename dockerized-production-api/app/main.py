from fastapi import FastAPI
from app.db import init_db
from app.core.config import settings

app = FastAPI(title="Dockerized Production API")

@app.on_event("startup")
async def on_startup():
    """
    Initialize the database on application startup
    """
    await init_db()
