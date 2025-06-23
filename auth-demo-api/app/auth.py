
from passlib.context import CryptContext
from .database import fake_users_db

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