from fastapi import FastAPI
from app.worker.tasks import fake_long_task

app = FastAPI()

@app.get("/ping")
async def ping():
    return {"message": "pong"}