from datetime import datetime
from typing import List
from pydantic import BaseModel


class TagCreate(BaseModel):
    """
    TagCreate model for creating a new tag
    """
    name: str

class TagRead(BaseModel):
    """
    TagRead model for reading tag data
    """
    id: int
    name: str

    class Config:
        from_attributes = True




class CommentCreate(BaseModel):
    """CommentCreate model for creating a new comment"""
    content: str


class CommentRead(BaseModel):
    """CommentRead model for reading comment data"""
    id: int
    content: str
    created_at: datetime

    class Config:
        from_attributes = True
        extra = "ignore"


        


class BlogPostCreate(BaseModel):
    """ BlogPostCreate model for creating a new blog post"""
    title: str
    content: str
    tag_ids: List[int] = []

class BlogPostRead(BaseModel):
    """BlogPostRead model for reading blog post data"""
    id: int
    title: str
    content: str
    created_at: datetime
    updated_at: datetime
    tags: List[TagRead] = []
    comments: List[CommentRead] = []

    class Config:
        from_attributes = True
        extra = "ignore"

class BlogPostReadNoComments(BaseModel):
    """BlogPostReadNoComments model for reading blog post data without comments"""
    id: int
    title: str
    content: str
    created_at: datetime
    updated_at: datetime
    tags: List[TagRead] = []

    class Config:
        from_attributes = True
        extra = "ignore"
