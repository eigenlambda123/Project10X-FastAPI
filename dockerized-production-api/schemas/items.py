# app/schemas/item.py
from datetime import datetime
from pydantic import BaseModel


class ItemBase(BaseModel):
    title: str
    description: str


class ItemCreate(ItemBase):
    pass


class ItemRead(ItemBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
