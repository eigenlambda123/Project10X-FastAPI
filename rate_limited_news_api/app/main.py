from fastapi import FastAPI
from .rate_limit import limiter, rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from .routers import news

def create_app():
    app = FastAPI()

    # Attach limiter + exception handler
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, rate_limit_exceeded_handler)

    # Register routes 
    app.include_router(news.router, prefix="/news")

    return app


app = create_app()