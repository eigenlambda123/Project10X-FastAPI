from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy import create_engine
from app.core.config import DATABASE_URL

# Async engine for FastAPI
async_engine = create_async_engine(DATABASE_URL, echo=True)
async_session = async_sessionmaker(async_engine, class_=AsyncSession, expire_on_commit=False)

# Sync engine for Celery worker
sync_engine = create_engine(DATABASE_URL.replace("+aiosqlite", ""), echo=True)

async def init_db():
    async with async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
