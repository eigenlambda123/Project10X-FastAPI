from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    weather_api_key: str
    weather_api_url: str

    class Config:
        env_file = ".env" # Load environment variables from .env file

settings = Settings()