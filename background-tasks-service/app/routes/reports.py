from fastapi import APIRouter, BackgroundTasks
from pydantic import BaseModel
from uuid import UUID

from app.utils import generate_task_id
from app.store import create_task_entry
from app.tasks import generate_report

router = APIRouter()

class ReportRequest(BaseModel):
    """Schema for Report Request use for validation"""
    name: str
    details: dict

@router.post("/")
async def generate_report_task(payload: ReportRequest, background_tasks: BackgroundTasks):
    """Endpoint to generate a report asynchronously"""

    task_id = generate_task_id() # Generate a unique task ID

    # Create a new task entry with task_type "report"
    create_task_entry(task_id, task_type="report", data=payload.dict()) 

    # Add the generate_report task to the background tasks
    # This will run asynchronously in the background and will be executed after the response is sent
    background_tasks.add_task(generate_report, task_id, payload.dict())

    return {"task_id": str(task_id), "status": "started"}