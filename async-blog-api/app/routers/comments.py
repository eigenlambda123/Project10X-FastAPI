from fastapi import APIRouter
from sqlmodel.ext.asyncio.session import AsyncSession

from app.db import async_session

router = APIRouter(prefix="/posts/{post_id}/comments", tags=["Comments"])

async def get_session() -> AsyncSession:
    async with async_session() as session:
        """Get an async session for database operations"""
        yield session

