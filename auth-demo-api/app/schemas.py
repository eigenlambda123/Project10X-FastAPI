from typing import Optional, Literal
from uuid import UUID
from pydantic import BaseModel, EmailStr, Field

# -- User Schema --

class UserBase(BaseModel):
    """Base schema for user data, used for creating and updating users"""
    username: str
    email: EmailStr
    role: Literal["user", "admin"] = "user" # default role is 'user' 
    is_active: bool = True