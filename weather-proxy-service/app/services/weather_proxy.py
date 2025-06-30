import httpx
from typing import Optional
from app.config import settings
from app.utils.cache import make_cache_key, get_from_cache, set_cache
import logging


class WeatherAPIError(Exception):
    """Custom error class for weather fetch failures"""

async def fetch_weather_data(city: Optional[str] = None, lat: Optional[float] = None, lon: Optional[float] = None):
    """
    Fetch weather data from the OpenWeatherMap API
    """


    # Check if city or lat/lon are provided
    if not city and (lat is None or lon is None): 
        raise ValueError("You must provide either a city or both latitude and longitude.")
    

    # Generate a cache key based on city or coordinates
    cache_key = make_cache_key(city=city, lat=lat, lon=lon)
    cached = get_from_cache(cache_key) # Retrieve data from cache
    # Log cache hit/miss
    if cached:
        logging.info(f"[CACHE HIT] {cache_key}") 
        return cached
    logging.info(f"[CACHE MISS] {cache_key}")


    
    # parameters for the API request
    params = {
        "appid": settings.weather_api_key,
        "units": "metric"
    }

    # If city is provided, use it; otherwise use lat/lon
    if city:
        params["q"] = city
    else:
        params["lat"] = lat
        params["lon"] = lon


    try:
        # Use an async HTTP client to fetch the weather data
        # Set a timeout for the request to avoid hanging indefinitely
        # Add cache handling
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(settings.weather_api_url, params=params)
            response.raise_for_status()
            result = response.json()
            set_cache(cache_key, result) # Store the result in cache
            return result

    except httpx.RequestError as e:
        raise WeatherAPIError(f"Request error: {e}") from e

    except httpx.HTTPStatusError as e:
        raise WeatherAPIError(f"API returned error {e.response.status_code}") from e



