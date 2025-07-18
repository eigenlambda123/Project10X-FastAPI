from fastapi import APIRouter, HTTPException
from sqlmodel import select
from app.db import async_session
from app.models import Task
from app.worker.tasks import long_task
from pydantic import BaseModel, HttpUrl
from typing import Optional

router = APIRouter()

class SubmitTaskRequest(BaseModel):
    webhook_url: Optional[str] = None


@router.post("/tasks/submit")
async def submit_task(payload: SubmitTaskRequest):
    """
    Post endpoint to submit a new task.
    
    This endpoint creates a new task record in the database and triggers a background long-running task.

    Optionally, you can provide a `webhook_url` in the request body. If provided, the system will send a POST request
    with the task result to the specified webhook URL once the task is completed.
    """
    new_task = Task(webhook_url=payload.webhook_url)
    async with async_session() as session:
        session.add(new_task)
        await session.commit()

    long_task.delay(new_task.id, 21)
    return {"task_id": new_task.id}


@router.get("/tasks/{task_id}/status")
async def get_status(task_id: str):
    """
    GET endpoint to check the status of a task by its ID.
    This endpoint retrieves the task from the database and returns its status.
    """
    async with async_session() as session:
        task = await session.get(Task, task_id)
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        return {"task_id": task.id, "status": task.status}
    

@router.get("/tasks/{task_id}/result")
async def get_result(task_id: str):
    """
    GET endpoint to retrieve the result of a completed task by its ID.
    This endpoint checks the status of the task and returns the result if it's successful
    or an appropriate message if the task is still in progress or has failed.
    """
    async with async_session() as session:
        task = await session.get(Task, task_id)
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        if task.status != "SUCCESS":
            return {"status": task.status, "result": None}
        return {"status": task.status, "result": task.result}