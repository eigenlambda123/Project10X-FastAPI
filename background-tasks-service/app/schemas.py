from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from datetime import datetime

class TaskStatus(BaseModel):
    """Schema for Task Status"""
    id: UUID
    type: str
    status: str
    result: Optional[dict]
    error: Optional[str]
    timestamp: datetime
