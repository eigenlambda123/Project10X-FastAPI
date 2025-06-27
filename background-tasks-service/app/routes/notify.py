from fastapi import APIRouter, BackgroundTasks
from pydantic import BaseModel, EmailStr
from app.utils import generate_task_id
from app.store import create_task_entry
from app.tasks import send_notification

router = APIRouter()

class NotifyRequest(BaseModel):
    """Schema for Notification Request"""
    email: EmailStr
    message: str


@router.post("/notify")
async def notify_user(payload: NotifyRequest, background_tasks: BackgroundTasks):
    """Endpoint to send a notification to a user via email"""

    task_id = generate_task_id() # Generate a unique task ID

    # Create a new task entry with task_type "notification"
    create_task_entry(task_id, task_type="notification", data=payload.dict())

    # Add the send_notification task to the background tasks
    # This will run asynchronously in the background and will be executed after the response is sent
    background_tasks.add_task(send_notification, task_id, payload.email, payload.message) 

    return {"task_id": str(task_id), "status": "started"}
