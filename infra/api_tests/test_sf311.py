# Test script: SF 311 Incidents API
# Confirms the API returns recent city service requests for San Francisco
# Usage: python3.11 infra/api_tests/test_sf311.py

import requests
import os
from dotenv import load_dotenv


load_dotenv()
app_token = os.getenv("SF_311_APP_TOKEN")

url = "https://data.sfgov.org/resource/vw6y-z8j6.json"
params = {
    "$limit": 10,
    "$order": "requested_datetime DESC"
}
headers = {
    "X-App-Token": app_token
}


response = requests.get(url, params=params, headers=headers)
data = response.json()

print("Status code:", response.status_code)
print("Number of records:", len(data))
print("\nFirst service request:")
print("  Type:", data[0].get("service_name"))
print("  Status:", data[0].get("status"))
print("  Requested:", data[0].get("requested_datetime"))
print("  Address:", data[0].get("address"))
