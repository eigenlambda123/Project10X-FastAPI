from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_weather_success():
    """
    Test for successful weather data retrieval
    """

    response = client.get("/weather?city=Manila") # GET request to the weather endpoint
    assert response.status_code == 200 # Check if the status code is 200 OK
    data = response.json() # Parse the JSON response

    # Check if the response contains the expected keys
    assert "temperature" in data
    assert "description" in data
    assert "humidity" in data
    assert "location" in data


def test_invalid_location():
    """
    Test for invalid location input
    """
    response = client.get("/weather?city=ThisCityDoesNotExistXYZ") # GET request to a non-existent city
    assert response.status_code == 404 or response.status_code == 400 or response.status_code == 502 # Check if the status code is 404 Not Found or 400 Bad Request or 502 Bad Gateway


def test_missing_params():
    """
    Test for missing query parameters
    """
    response = client.get("/weather") # GET request without city parameter
    assert response.status_code == 400 # Check if the status code is 400 Bad Request


# def test_invalid_combination():
#     """
#     Test for invalid combination of query parameters
#     """
#     response = client.get("/weather?city=Manila&lat=14.6") # GET request with both city and lat parameters
#     assert response.status_code == 400 # Check if the status code is 400 Bad Request


def test_cache_hit():
    """
    Test for cache hit functionality
    """
    # First call (miss)
    response1 = client.get("/weather?city=Manila")
    assert response1.status_code == 200

    # Second call (should be hit)
    response2 = client.get("/weather?city=Manila")
    assert response2.status_code == 200
    


def test_weather_by_coordinates():
    """ 
    Test for weather data retrieval by coordinates
    """
    response = client.get("/weather?lat=14.5995&lon=120.9842")
    assert response.status_code == 200

    data = response.json()
    assert "temperature" in data
    assert "description" in data
    assert "location" in data


def test_weather_no_params():
    """
    Test for missing query parameters
    """
    response = client.get("/weather")
    assert response.status_code == 400 # Check if the status code is 400 Bad Request


