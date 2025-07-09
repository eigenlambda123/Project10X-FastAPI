from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field


class PostTagLink(SQLModel, table=True):
    """
    PostTagLink model representing the association between blog posts and tags
    Attributes:
        post_id (Optional[int]): Unique identifier for the blog post.
        tag_id (Optional[int]): Unique identifier for the tag.
    """
    post_id: Optional[int] = Field(default=None, foreign_key="blogpost.id", primary_key=True)
    tag_id: Optional[int] = Field(default=None, foreign_key="tag.id", primary_key=True)


class BlogPost(SQLModel, table=True):
    """
    BlogPost model representing a blog post in the database
    Attributes:
        id (Optional[int]): Unique identifier for the blog post.
        title (str): Title of the blog post.
        content (str): Content of the blog post.
        created_at (datetime): Timestamp when the blog post was created.
        updated_at (datetime): Timestamp when the blog post was last updated.
    """

    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    content: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class Tag(SQLModel, table=True):
    """
    Tag model representing a tag in the database
    Attributes:
        id (Optional[int]): Unique identifier for the tag.
        name (str): Name of the tag.
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str