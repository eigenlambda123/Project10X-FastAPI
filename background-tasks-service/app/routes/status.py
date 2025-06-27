from fastapi import APIRouter, HTTPException
from uuid import UUID

from app.store import get_task
from app.schemas import TaskStatus

router = APIRouter()

@router.get("/{task_id}", response_model=TaskStatus)
async def check_task_status(task_id: UUID):
    """Endpoint to check the status of a task by its ID"""
    task = get_task(task_id) # get task by id
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    # Return the task status
    # This will return the task ID, type, status, result, error (if any), and timestamp
    return {
        "id": task_id,
        "type": task["type"],
        "status": task["status"],
        "result": task["result"],
        "error": task["error"],
        "timestamp": task["timestamp"]
    }