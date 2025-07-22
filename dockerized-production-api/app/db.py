from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from app.core.config import settings

# Create an async SQLAlchemy engine
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=True,
    future=True,
    )

# Create an async session factory
async_session_factory = async_sessionmaker(
    engine, expire_on_commit=False, class_=AsyncSession
)


# dependency to get a session
async def get_session() -> AsyncSession:
    async with async_session_factory() as session:
        yield session


# For table creation at startup
async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)