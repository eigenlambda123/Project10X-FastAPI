from fastapi import APIRouter, Depends
from app.deps import get_current_user, get_current_admin
from app.schemas import UserOut
from uuid import UUID

router = APIRouter()


@router.get("/me", response_model=UserOut)
async def read_current_user(current_user: dict = Depends(get_current_user)):
    """Get the current logged-in user"""
    return current_user

@router.get("/admin", response_model=UserOut)
async def read_admin_data(current_admin: dict = Depends(get_current_admin)):
    """Get data accessible only by admin users"""
    return current_admin