from fastapi import APIRouter, Query, HTTPException
from typing import Optional
from app.services.weather_proxy import fetch_weather_data, WeatherAPIError

router = APIRouter()

@router.get("/weather")
async def get_weather(
    city: Optional[str] = Query(None),
    lat: Optional[float] = Query(None),
    lon: Optional[float] = Query(None),
):
    """Get weather data for a specified city or latitude/longitude"""

    try:
        # Fetch weather data from the OpenWeatherMap API using city or lat/lon
        data = await fetch_weather_data(city=city, lat=lat, lon=lon)
        return {
            "source": "OpenWeatherMap",
            "location": data.get("name"),
            "temperature": data.get("main", {}).get("temp"),
            "description": data.get("weather", [{}])[0].get("description"),
            "humidity": data.get("main", {}).get("humidity"),
            "wind_speed": data.get("wind", {}).get("speed"),
        }

    # Exceptions
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    except WeatherAPIError as e:
        raise HTTPException(status_code=502, detail=str(e))