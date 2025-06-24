from fastapi import APIRouter
from fastapi import HTTPException, status
from app.schemas import UserCreate
from app.database import fake_users_db, hash_password
from app.auth import create_access_token
from uuid import uuid4

router = APIRouter()

@router.post("/login")
async def login():
    return {"message": "Login endpoint"}


@router.post("/register")
async def register(user: UserCreate):
    """Register a new user"""

    # Check if user already exists
    if user.username in fake_users_db or any(u["email"] == user.email for u in fake_users_db.values()):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username or email already registered."
        )
    
    # Create a new user entry
    new_user = {
        "id": str(uuid4()), # generate a unique ID for the user
        "username": user.username,
        "email": user.email,
        "hashed_password": hash_password(user.password), # hash the password
        "is_active": True,
        "role": user.role
    }
    fake_users_db[user.username] = new_user # add the new user to the fake database username as key and new_user as value

    # Create token
    access_token = create_access_token(
        data={"sub": new_user["username"], "role": new_user["role"]}
    )
    return {"access_token": access_token, "token_type": "bearer"} # return the access token and token type