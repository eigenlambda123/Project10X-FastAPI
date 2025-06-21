from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from uuid import UUID

class BookBase(BaseModel):
    """Base model for Book schema"""
    title: str = Field(..., max_length=100) # Title of the book
    author: str = Field(..., max_length=100) # Author of the book
    genre: Optional[str] = Field(None, max_length=50) # Genre of the book, optional
    published_year: int = Field(..., ge=0) # Year the book was published, must be a positive integer




