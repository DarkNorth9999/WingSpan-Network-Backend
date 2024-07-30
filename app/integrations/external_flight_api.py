import requests
from datetime import datetime

def fetch_flight_details(flight_number: str, date: datetime, departure_airport: str, arrival_airport: str):
    url = "https://airlabs.co/api/v9/schedules"
    params = {
        "api_key": "YOUR_API_KEY",
        "flight_iata": flight_number,
        "dep_iata": departure_airport,
        "arr_iata": arrival_airport,
        "date": date.strftime('%Y-%m-%d')
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": "Failed to fetch flight details"}

# Note: Ensure you handle API errors and exceptions appropriately.
