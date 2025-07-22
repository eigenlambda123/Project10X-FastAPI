from fastapi import APIRouter, Depends, Query
from app.db import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select

from app.models.item import Item
from app.schemas.items import ItemCreate, ItemRead


router = APIRouter(prefix="/items", tags=["Items"])


@router.post("/", response_model=ItemRead, status_code=201)
async def create_item(item: ItemCreate, session: AsyncSession = Depends(get_session)):
    """
    POST endpoint to create a new item
    """
    db_item = Item(**item.model_dump())
    session.add(db_item)
    await session.commit()
    await session.refresh(db_item)
    return db_item


@router.get("/", response_model=list[ItemRead])
async def list_items(
    limit: int = Query(default=10, le=100),
    offset: int = Query(default=0, ge=0),
    session: AsyncSession = Depends(get_session),
):
    """
    GET endpoint to list items with pagination
    """
    result = await session.exec(select(Item).offset(offset).limit(limit))
    items = result.all()
    return items