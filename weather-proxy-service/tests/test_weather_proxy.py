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

