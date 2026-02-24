# Test script: 511.org Transit API
# Confirms the API returns real-time vehicle arrival predictions for SF Muni
# Usage: python3.11 infra/api_tests/test_511.py

import requests
import os
from dotenv import load_dotenv
import json

load_dotenv()
api_key = os.getenv("API_511_TOKEN")

url = "https://api.511.org/transit/StopMonitoring"
params = {
    "api_key": api_key,
    "agency": "SF",
    "format": "json"
}


response = requests.get(url, params=params)
data = json.loads(response.content.decode("utf-8-sig"))

print("Status code:", response.status_code)
print("Agency:", data["ServiceDelivery"]["StopMonitoringDelivery"]["MonitoredStopVisit"][0]["MonitoredVehicleJourney"]["OperatorRef"])
print("Line:", data["ServiceDelivery"]["StopMonitoringDelivery"]["MonitoredStopVisit"][0]["MonitoredVehicleJourney"]["LineRef"])
print("Destination:", data["ServiceDelivery"]["StopMonitoringDelivery"]["MonitoredStopVisit"][0]["MonitoredVehicleJourney"]["DestinationName"])
print("Expected arrival:", data["ServiceDelivery"]["StopMonitoringDelivery"]["MonitoredStopVisit"][0]["MonitoredVehicleJourney"]["MonitoredCall"]["ExpectedArrivalTime"])
