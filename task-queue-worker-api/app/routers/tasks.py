from fastapi import APIRouter, HTTPException
from sqlmodel import select
from app.db import async_session
from app.models import Task
from app.worker.tasks import long_task

router = APIRouter()

@router.post("/tasks/submit")
async def submit_task():
    """
    POST endpoint for submitting a new task to the queue and returning the task ID.
    This endpoint creates a new Task instance, saves it to the database,
    and enqueues it for processing in the Celery worker.
    """
    new_task = Task()
    async with async_session() as session:
        session.add(new_task)
        await session.commit()

    long_task.delay(new_task.id, 21)
    return {"task_id": new_task.id}