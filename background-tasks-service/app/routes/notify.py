from fastapi import APIRouter, BackgroundTasks
from pydantic import BaseModel, EmailStr

router = APIRouter()

class NotifyRequest(BaseModel):
    """Schema for Notification Request"""
    email: EmailStr
    message: str

@router.post("/")
def notify_user(background_tasks: BackgroundTasks):
    # stub - real logic will come later
    return {"message": "Notification task triggered"}
