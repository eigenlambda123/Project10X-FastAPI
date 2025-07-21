from fastapi import FastAPI
from app.routers import redis_test

app = FastAPI()

app.include_router(redis_test.router)
