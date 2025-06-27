from fastapi import APIRouter, BackgroundTasks
from pydantic import BaseModel

router = APIRouter()

class ReportRequest(BaseModel):
    """Schema for Report Request use for validation"""
    name: str
    details: dict

@router.post("/")
def generate_report(background_tasks: BackgroundTasks):
    # stub - real logic will come later
    return {"message": "Report generation task triggered"}