from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field

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