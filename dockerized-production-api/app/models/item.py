# app/models/item.py
from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional


class Item(SQLModel, table=True):
    """Item model for the database"""
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    description: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
