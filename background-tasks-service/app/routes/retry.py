from fastapi import APIRouter, BackgroundTasks, HTTPException
from uuid import UUID

from app.store import get_task, update_task_status
from app.tasks import send_notification, generate_report

router = APIRouter()

@router.post("/retry-task/{task_id}")
async def retry_task(task_id: UUID, background_tasks: BackgroundTasks):
    """
    Retry a failed background task by its ID.

    This endpoint allows clients to retry a task that previously failed. It performs the following steps:
    - Looks up the task by its UUID
    - Ensures the task exists and is in a 'failed' state
    - Increments the retry count and resets the task's status, error, and result fields
    - Schedules the appropriate background task (notification or report) for re-execution
    - Returns the task ID and a status indicating the retry was initiated
    """

    task = get_task(task_id) # get the task from the store by its ID

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    if task["status"] != "failed":
        raise HTTPException(status_code=400, detail="Only failed tasks can be retried")

    # Increment retry count
    task["retries"] += 1
    task["status"] = "pending"
    task["error"] = None
    task["result"] = None

    # Re-run the appropriate task
    if task["type"] == "notification": # check if the task type is notification
        background_tasks.add_task(send_notification, task_id, task["data"]["email"], task["data"]["message"])

    elif task["type"] == "report": # check if the task type is report
        background_tasks.add_task(generate_report, task_id, task["data"])
        
    else:
        raise HTTPException(status_code=400, detail="Retry not supported for this task type")

    return {"task_id": str(task_id), "status": "retried"}
