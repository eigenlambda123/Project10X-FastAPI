from fastapi import FastAPI
from app.routers import test, users

app = FastAPI()


app.include_router(test.router)
app.include_router(users.router, prefix="/api", tags=["users"])