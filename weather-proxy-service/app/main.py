from fastapi import FastAPI
from app.api.routes import router as weather_router

app = FastAPI(
    title="Weather Proxy Microservice",
    description="Proxies OpenWeatherMap data with caching and transformation.",
    version="0.1.0"
)

app.include_router(weather_router) # Include the weather router