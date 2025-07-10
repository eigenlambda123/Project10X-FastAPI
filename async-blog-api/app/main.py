from fastapi import FastAPI
from app.db import create_db_and_tables
from app.routers import posts, tags

app = FastAPI()

@app.on_event("startup")
async def on_startup():
    await create_db_and_tables()

app.include_router(posts.router) 
app.include_router(tags.router)