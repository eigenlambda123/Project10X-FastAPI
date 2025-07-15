from fastapi import FastAPI
from app.routers import tasks
from app.db import init_db

app = FastAPI()

@app.get("/ping")
async def ping():
    return {"message": "pong"}


@app.on_event("startup")
async def startup():
    await init_db()


app.include_router(tasks.router, prefix="/api", tags=["tasks"])
