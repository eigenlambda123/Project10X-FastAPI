from fastapi import APIRouter, Depends
from app.db import get_session
from sqlmodel.ext.asyncio.session import AsyncSession

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