from fastapi import APIRouter, Depends, HTTPException
from app.models import Comment, BlogPost
from app.schemas import CommentRead, CommentCreate
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from typing import List
from app.core.auth import get_current_admin_user


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



@router.post("/", response_model=CommentRead)
async def create_comment(
    post_id: int,
    comment: CommentCreate,
    session: AsyncSession = Depends(get_session)
):
    """
    POST endpoint to create a new comment on a blog post
    Args:
        post_id (int): The ID of the blog post to add a comment to
        comment (CommentCreate): The comment data to create
    """
    # get to check if the post exists via post_id
    # if the post does not exist, raise a 404 error
    post = await session.get(BlogPost, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    # create a new comment instance and associate it with the post_id
    db_comment = Comment(post_id=post_id, content=comment.content)
    session.add(db_comment)
    await session.commit()
    await session.refresh(db_comment)
    return db_comment



@router.delete("/{id}")
async def delete_comment(
    id: int,
    session: AsyncSession = Depends(get_session),
    _: dict = Depends(get_current_admin_user)
):
    """
    DELETE endpoint to delete a comment by ID (only accessible by admin users)
    Args:
        id (int): The ID of the comment to delete
        session (AsyncSession): The database session
        _: dict: Dependency to ensure the user is an admin
    """
    comment = await session.get(Comment, id)
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    await session.delete(comment)
    await session.commit()
    return {"detail": "Comment deleted"}
