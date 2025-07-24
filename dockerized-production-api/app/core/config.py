from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """
    Application settings loaded from environment variables
    """
    DATABASE_URL: str
    ENV: str = "development"

    class Config:
        env_file = ".env"
        extra = "allow"

settings = Settings()
