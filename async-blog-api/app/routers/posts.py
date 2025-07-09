from fastapi import Depends, APIRouter
from app.db import async_session
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.models import BlogPost, Tag
from app.schemas import BlogPostCreate, BlogPostRead

router = APIRouter(prefix="/posts", tags=["Posts"])


async def get_session() -> AsyncSession:
    """
    Get an async session for database operations
    """
    async with async_session() as session:
        yield session


@router.post("/", response_model=BlogPostRead)
async def create_post(post: BlogPostCreate, session: AsyncSession = Depends(get_session)):
    """ 
    POST endpoint to create a new blog post
    Args:
        post (BlogPostCreate): The blog post data to create
        session (AsyncSession): The database session
    """
    db_post = BlogPost(title=post.title, content=post.content)

    # if there are tags, attach them via the relationship
    if post.tag_ids:
        tags = await session.exec(select(Tag).where(Tag.id.in_(post.tag_ids)))
        db_post.tags = tags.all()
    
    session.add(db_post)
    await session.commit()
    await session.refresh(db_post, attribute_names=["tags"])
    return db_post


@router.get("/", response_model=List[BlogPostRead])
async def read_posts(session: AsyncSession = Depends(get_session)):
    """
    GET endpoint to read all blog posts
    Args:
        session (AsyncSession): The database session
    """
    result = await session.exec(select(BlogPost))
    return result.all()