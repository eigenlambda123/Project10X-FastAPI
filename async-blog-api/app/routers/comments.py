from fastapi import APIRouter, Depends
from app.models import Comment
from app.schemas import CommentRead
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from typing import List


from app.db import async_session

router = APIRouter(prefix="/posts/{post_id}/comments", tags=["Comments"])

async def get_session() -> AsyncSession:
    async with async_session() as session:
        """Get an async session for database operations"""
        yield session



@router.get("/", response_model=List[CommentRead])
async def read_comments(post_id: int, session: AsyncSession = Depends(get_session)):
    """
    GET endpoint to read all comments for a specific blog post
    Args:
        post_id (int): The ID of the blog post to read comments for
        session (AsyncSession): The database session
    """
    result = await session.exec(
        select(Comment).where(Comment.post_id == post_id)
    )
    return result.all()