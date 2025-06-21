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


class BookCreate(BookBase):
    """Schema for creating a new book that inherits from BookBase"""
    pass


class BookUpdate(BookBase):
    """Schema for updating an existing book that inherits from BookBase"""
    pass


class Book(BookBase):
    """Schema for Book response, including reviews"""
    id: UUID
    reviews: Optional[List["Review"]] = [] # List of reviews associated with the book

    class Config:
        orm_mode = True 


class ReviewBase(BaseModel):
    """Base model for Review schema"""
    reviewer: str = Field(..., max_length=100) # Name of the reviewer
    rating: int = Field(..., ge=1, le=5) # Rating given by the reviewer, must be between 1 and 5
    text: Optional[str] = None # Review text, optional


class ReviewSummary(BaseModel):
    """Schema for summarizing reviews of a book"""
    book_id: UUID # ID of the book
    average_rating: float # Average rating of the book
    total_reviews: int # Total number of reviews for the book




