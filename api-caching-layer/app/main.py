from fastapi import FastAPI
from app.routers import test, users, posts, cache_admin

app = FastAPI()


app.include_router(test.router)
app.include_router(users.router, prefix="/api", tags=["users"])
app.include_router(posts.router, prefix="/api", tags=["posts"])
app.include_router(cache_admin.router, prefix="/api/admin", tags=["cache_admin"])