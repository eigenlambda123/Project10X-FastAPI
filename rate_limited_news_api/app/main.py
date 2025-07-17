from fastapi import FastAPI
from slowapi.middleware import SlowAPIMiddleware
from .rate_limit import limiter
from .routers import news

app = FastAPI()
app.state.limiter = limiter
app.add_middleware(SlowAPIMiddleware)

app.include_router(news.router)