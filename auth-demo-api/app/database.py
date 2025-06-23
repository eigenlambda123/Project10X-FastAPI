from uuid import uuid4
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Function for Hashing passwords
def hash_password(password: str) -> str:
    """Hash a password using bcrypt"""
    return pwd_context.hash(password)


# Simulated user storage
fake_users_db: dict[str, dict] = {
    "johndoe": {
        "id": str(uuid4()),
        "username": "johndoe",
        "email": "johndoe@example.com",
        "hashed_password": hash_password("secret123"),
        "is_active": True,
        "role": "user"
    },
    "admin": {
        "id": str(uuid4()),
        "username": "admin",
        "email": "admin@example.com",
        "hashed_password": hash_password("adminpass"),
        "is_active": True,
        "role": "admin"
    }
}