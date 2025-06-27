from fastapi import APIRouter, BackgroundTasks
from pydantic import BaseModel
from uuid import UUID

from app.utils import generate_task_id
from app.store import create_task_entry
from app.tasks import generate_file

router = APIRouter()

class FileRequest(BaseModel):
    """Schema for File Generation Request"""
    content: dict

@router.post("/")
async def generate_file_task(payload: FileRequest, background_tasks: BackgroundTasks):
    """Endpoint to generate a file from the provided content"""

    task_id = generate_task_id() # Generate a unique task ID
    create_task_entry(task_id, task_type="file", data=payload.dict()) # Create a new task entry with task_type "file"

    # Add the generate_file task to the background tasks
    # This will run asynchronously in the background and will be executed after the response is sent
    background_tasks.add_task(generate_file, task_id, payload.content) 

    return {"task_id": str(task_id), "status": "started"}
