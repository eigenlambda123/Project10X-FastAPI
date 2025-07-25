from fastapi import APIRouter, Depends
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from typing import List

from app.db import async_session
from app.models import Tag
from app.schemas import TagCreate, TagRead

router = APIRouter(prefix="/tags", tags=["Tags"])

async def get_session() -> AsyncSession:
    """
    Get an async session for database operations
    """
    async with async_session() as session:
        yield session

@router.post("/", response_model=TagRead)
async def create_tag(tag: TagCreate, session: AsyncSession = Depends(get_session)):
    """
    POST endpoint to create a new tag
    """
    db_tag = Tag(name=tag.name)
    session.add(db_tag)
    await session.commit()
    await session.refresh(db_tag)
    return TagRead.model_validate(db_tag)


@router.get("/", response_model=List[TagRead])
async def read_tags(session: AsyncSession = Depends(get_session)):
    """
    GET endpoint to read all tags
    """
    result = await session.exec(select(Tag))
    tags = result.all()
    return [TagRead.model_validate(tag) for tag in tags]