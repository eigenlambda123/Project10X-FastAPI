from fastapi import FastAPI
from app.db import create_db_and_tables
from app.routers import posts, tags, comments
import jwt

app = FastAPI()

# Example JWT token generation for an admin user
token = jwt.encode({"sub": "admin@example.com", "is_admin": True}, "your-secret-key", algorithm="HS256")
print(f"Token: {token}")

@app.on_event("startup")
async def on_startup():
    await create_db_and_tables()

app.include_router(posts.router) 
app.include_router(tags.router)
app.include_router(comments.router)