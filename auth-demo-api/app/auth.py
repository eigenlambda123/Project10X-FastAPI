
from passlib.context import CryptContext
from .database import fake_users_db
from datetime import datetime, timedelta
from jose import jwt

SECRET_KEY = "secret"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# -- Utility Functions --

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against a hashed password."""
    return pwd_context.verify(plain_password, hashed_password)

def get_user_by_username(username: str) -> dict | None:
    """Get a user by their username"""
    return fake_users_db.get(username)

def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    """Create a JWT access token with an expiration time"""

    # copy the data to avoid modifying the original
    to_encode = data.copy() 

    # default to 30 minutes if no expiration is provided
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)) 

    # add the expiration time to the token data
    to_encode.update({"exp": expire}) 

    # encode the token with the secret key and algorithm
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM) 