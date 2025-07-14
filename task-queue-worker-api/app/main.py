from fastapi import FastAPI
from app.worker.tasks import fake_long_task

app = FastAPI()

@app.get("/ping")
async def ping():
    return {"message": "pong"}

@app.post("/test-task")
async def run_test_task():
    task = fake_long_task.delay(42)
    return {"message": "Task submitted", "task_id": task.id}
