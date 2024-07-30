import json
from datetime import datetime

def load_flight_data():
    with open('integrations/flight_data.json', 'r') as file:
        data = json.load(file)
    return data

def search_flights(flight_number=None, date=None, origin=None, destination=None):
    flights = load_flight_data()
    filtered_flights = []
    for flight in flights:
        if flight_number and flight['flight_number'] == flight_number:
            filtered_flights.append(flight)
            break
        if date and datetime.strptime(flight['scheduled_departure'], '%Y-%m-%dT%H:%M:%SZ').date() != date:
            continue
        if origin and flight['origin'] != origin:
            continue
        if destination and flight['destination'] != destination:
            continue

    return filtered_flights

