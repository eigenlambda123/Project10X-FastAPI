from pydantic import BaseModel

class WeatherResponse(BaseModel):
    """Schema for the weather response data"""
    source: str
    location: str
    temperature: float
    description: str
    humidity: int
    wind_speed: float
