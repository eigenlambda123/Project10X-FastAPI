from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

SECRET_KEY = "secret"
ALGORITHM = "HS256"


def decode_token(token: str):
    """
    Decode JWT token to extract user information
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload  # contains "sub", "is_admin", etc.
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")