from fastapi import Depends, APIRouter
from sqlmodel.ext.asyncio.session import AsyncSession
from app.db import async_session

from app.models import BlogPost, Tag, PostTagLink
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
    """

    db_post = BlogPost(title=post.title, content=post.content)
    session.add(db_post)
    await session.commit()
    await session.refresh(db_post)
    return db_post