from sqlmodel import SQLModel, Field
from datetime import datetime
from uuid import uuid4
from typing import Optional

class Task(SQLModel, table=True):
    """
    Task model representing a unit of work in the system
    """
    id: str = Field(default_factory=lambda: str(uuid4()), primary_key=True)
    status: str = Field(default="PENDING")
    result: str | None = None
    webhook_url: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
