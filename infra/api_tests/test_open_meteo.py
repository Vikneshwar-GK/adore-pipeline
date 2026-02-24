# Test script: Open-Meteo Weather API
# Confirms the API returns hourly weather data for San Francisco
# Usage: python3.11 infra/api_tests/test_open_meteo.py

import requests

url = "https://api.open-meteo.com/v1/forecast"
params = {
    "latitude": 37.7749,
    "longitude": -122.4194,
    "hourly": "temperature_2m,precipitation,windspeed_10m,relativehumidity_2m"
}


response = requests.get(url, params=params)
data = response.json()

print("Status code:", response.status_code)
print("Location:", data.get("latitude"), data.get("longitude"))
print("First 3 hourly temperatures (°C):", data["hourly"]["temperature_2m"][:3])
print("First 3 precipitation values:", data["hourly"]["precipitation"][:3])
print("First 3 wind speeds:", data["hourly"]["windspeed_10m"][:3])