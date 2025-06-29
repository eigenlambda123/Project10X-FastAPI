from fastapi import APIRouter, Query, HTTPException
from typing import Optional
from app.services.weather_proxy import fetch_weather_data, WeatherAPIError
from app.schemas.weather import WeatherResponse

router = APIRouter()

@router.get("/weather", response_model=WeatherResponse)
async def get_weather(
    city: Optional[str] = Query(None),
    lat: Optional[float] = Query(None),
    lon: Optional[float] = Query(None),
):
    """Get weather data for a specified city or latitude/longitude"""

    try:
        # Fetch weather data from the OpenWeatherMap API using city or lat/lon
        data = await fetch_weather_data(city=city, lat=lat, lon=lon)

        # return a structured response using the WeatherResponse schema
        return WeatherResponse(
            source="OpenWeatherMap",
            location=data.get("name"),
            temperature=data["main"]["temp"],
            description=data["weather"][0]["description"],
            humidity=data["main"]["humidity"],
            wind_speed=data["wind"]["speed"],
        )

    # Exceptions
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    except WeatherAPIError as e:
        raise HTTPException(status_code=502, detail=str(e))