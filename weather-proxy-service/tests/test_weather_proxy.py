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