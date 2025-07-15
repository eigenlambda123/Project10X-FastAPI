from fastapi import FastAPI
from app.routers import tasks

app = FastAPI()

@app.get("/ping")
async def ping():
    return {"message": "pong"}

app.include_router(tasks.router, prefix="/api", tags=["tasks"])
