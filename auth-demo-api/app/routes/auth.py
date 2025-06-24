from fastapi import APIRouter
from fastapi import HTTPException, status, Depends
from app.schemas import UserCreate, Token, LoginRequest
from app.database import fake_users_db, hash_password
from app.auth import create_access_token, verify_password
from uuid import uuid4
from fastapi.security import OAuth2PasswordRequestForm


router = APIRouter()


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




@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """Login a user and return an access token"""

    # Check if user exists and is active
    user = fake_users_db.get(form_data.username)
    if not user or not user["is_active"]:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Check if password is valid
    if not verify_password(form_data.password, user["hashed_password"]):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid username or password"
            )

    # Create access token
    access_token = create_access_token(
        data={"sub": user["username"], "role": user["role"]}
    )

    # Return the access token
    return {"access_token": access_token, "token_type": "bearer"}