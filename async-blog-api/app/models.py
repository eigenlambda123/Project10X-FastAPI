from datetime import datetime
from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship


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

    # Relationship to tags through the PostTagLink association table
    tags: List["Tag"] = Relationship(back_populates="posts", link_model=PostTagLink)

    # One-to-Many Relationship to comments
    comments: List["Comment"] = Relationship(back_populates="post")


class Tag(SQLModel, table=True):
    """
    Tag model representing a tag in the database
    Attributes:
        id (Optional[int]): Unique identifier for the tag.
        name (str): Name of the tag.
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str

    # Relationship to blog posts through the PostTagLink association table
    posts: List[BlogPost] = Relationship(back_populates="tags", link_model=PostTagLink)



class Comment(SQLModel, table=True):
    """
    Comment model representing a comment on a blog post
    Attributes:
        id (Optional[int]): Unique identifier for the comment.
        post_id (int): Foreign key referencing the blog post.
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    post_id: int = Field(foreign_key="blogpost.id")
    content: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship to the blog post
    post: Optional[BlogPost] = Relationship(back_populates="comments")