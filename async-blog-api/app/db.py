from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

# Database URL for SQLite using async support
DATABASE_URL = "sqlite+aiosqlite:///./blog.db"

# async SQLAlchemy engine
engine = create_async_engine(DATABASE_URL, echo=True)

# async session factory
async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

# Function to create the database and tables
async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
