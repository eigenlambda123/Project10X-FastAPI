from sqlmodel.ext.asyncio.session import AsyncSession
from app.db import async_session

async def get_session() -> AsyncSession:
    """
    Get an async session for database operations
    """
    async with async_session() as session:
        yield session
