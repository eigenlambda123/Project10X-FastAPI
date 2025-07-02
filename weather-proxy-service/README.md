# About Weather Proxy Microservice

A lightweight weather proxy service built with **FastAPI**, designed to fetch current weather data from a third-party API (OpenWeatherMap) and serve it through a clean, consistent interface. This project showcases **external API integration**, **parameter validation**, **response transformation**, and **in-memory caching** with TTL — all while maintaining a modular and testable design.

---

## Route Documentation

This API allows you to query for **current weather** data by city or coordinates. It acts as a **proxy**, abstracting the third-party API and transforming its response into a unified schema.

---

### **GET /weather?city=Manila**

**Description:** Retrieves weather for a given city name.

**Query Parameters:**

| Name | Type   | Required | Description             |
| ---- | ------ | -------- | ----------------------- |
| city | string | ✅        | Name of the target city |

**Response: 200 OK**

```json
{
  "location": "Manila",
  "temperature": 30.15,
  "feels_like": 32.5,
  "humidity": 70,
  "description": "clear sky"
}
```

---

### **GET /weather?lat=14.6\&lon=120.9**

**Description:** Retrieves weather using latitude and longitude.

**Query Parameters:**

| Name | Type  | Required | Description           |
| ---- | ----- | -------- | --------------------- |
| lat  | float | ✅        | Latitude of location  |
| lon  | float | ✅        | Longitude of location |

**Response: 200 OK**

Same structure as city-based response.

---

### Error Handling

| Scenario                      | Status Code   | Notes                                   |
| ----------------------------- | ------------- | --------------------------------------- |
| Missing all parameters        | `400`         | Must provide either `city` or `lat/lon` |
| Invalid city name             | `404/400/502` | Depends on API response or failure      |
| Mixed parameters (city + lat) | `400`         | Only one type of input allowed          |

---

## Features

| Feature                   | Description                                                    |
| ------------------------- | -------------------------------------------------------------- |
| **External API Proxy**    | Uses `httpx.AsyncClient` to call OpenWeatherMap                |
| **Env-Based Config**      | API key and base URL managed via `.env` and `BaseSettings`     |
| **Validation Layer**      | Custom logic ensures safe and correct parameter usage          |
| **Schema Transformation** | Converts raw API data into a clean, predictable JSON response  |
| **Caching**               | In-memory cache with TTL (e.g. 10 minutes) to reduce API usage |
| **Testing**               | Integration tests using FastAPI’s `TestClient`                 |

---

## Caching Behavior

The service caches responses by key (either city or lat/lon pair) using a simple dictionary with expiration timestamps. This reduces unnecessary external API calls and improves latency.

| Event         | Behavior                        |
| ------------- | ------------------------------- |
| First request | Fetches from API, caches result |
| Next request  | If within TTL, returns cached   |
| TTL expires   | Refetches and recaches          |

Cache behavior can be observed via logs showing cache **hit/miss**.

---

## Example `.env`

```
WEATHER_API_KEY=your_openweathermap_key_here
WEATHER_API_URL=https://api.openweathermap.org/data/2.5/weather
```

Use `python-dotenv` to load environment variables into your config.

---

## Project Structure

```
weather_proxy_service/
├── app/
│   ├── main.py
│   ├── api/
│   │   └── routes.py
│   ├── services/
│   │   └── weather_proxy.py
│   ├── schemas/
│   │   └── weather.py
│   ├── utils/
│   │   └── cache.py
│   └── config.py
├── tests/
│   └── test_weather_proxy.py
├── .env
└── requirements.txt
```

---

## Tests

Tests are written using `TestClient` to verify API correctness.

#### Covered Scenarios:

* Valid city and coordinates queries
* Missing parameters
* Invalid city names
* Cache hit behavior
* (Optional) Query validation edge cases

You can run tests with:

```bash
pytest tests/
```

---

## Notes

* You can expand this project to include:

  * **Forecast endpoints**
  * **Failover APIs**
  * **Circuit breakers** with `aiobreaker`
  * **Redis cache** (instead of in-memory)

* Designed to simulate a **real-world microservice pattern**, focused on clean interfaces and defensive programming.
