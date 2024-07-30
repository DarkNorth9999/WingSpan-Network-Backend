import schedule
import time
from datetime import datetime, timedelta
from app.database import get_db
from app.models.flight import Flight
from app.services.flight_service import search_flights
from app.models.notification import Notification
import requests
import json
from app.kafka.producer import producer

async def check_flights_update():
    print('check')
    db_gen = get_db()
    session = next(db_gen)

    check_time = datetime.now() - timedelta(hours=4)

    flights = session.query(Flight).filter(Flight.last_updated <= check_time,
                                           Flight.subscription_count > 0).all()


    for flight in flights:
        print(flight.last_updated)
        current_flight_data = search_flights(flight.flight_number, flight.scheduled_departure, flight.origin, flight.destination)
        if current_flight_data:
            await compare_and_update_flight(flight, current_flight_data, session)


async def compare_and_update_flight(flight, api_data, session):
    api_data = api_data[0]
    differences = []
    fields_to_update = {}

    if compare_datetimes(flight.actual_departure, api_data['actual_departure']):
        differences.append(("Departure change",
                            f"Flight {flight.flight_number} from {flight.origin} to {flight.destination}, scheduled to depart at {flight.scheduled_departure}, has a departure change from {flight.actual_departure} to {convert_iso_to_standard(api_data['actual_departure'])}"))
        fields_to_update['actual_departure'] = api_data['actual_departure']
    if compare_datetimes(flight.actual_arrival, api_data['actual_arrival']):
        differences.append(("Arrival change",
                            f"Flight {flight.flight_number} from {flight.origin} to {flight.destination}, scheduled to arrive at {flight.scheduled_arrival}, has an arrival change from {flight.actual_arrival} to {convert_iso_to_standard(api_data['actual_arrival'])}"))
        fields_to_update['actual_arrival'] = api_data['actual_arrival']
    if flight.status != api_data['status']:
        differences.append(("Status change",
                            f"Flight {flight.flight_number} from {flight.origin} to {flight.destination}, scheduled to depart at {flight.scheduled_departure}, has a status change from {flight.status} to {api_data['status']}"))
        fields_to_update['status'] = api_data['status']
    if flight.departure_gate != api_data['departure_gate']:
        differences.append(("Departure gate change",
                            f"Flight {flight.flight_number} from {flight.origin} to {flight.destination}, scheduled to depart at {flight.scheduled_departure}, has a departure gate change from {flight.departure_gate} to {api_data['departure_gate']}"))
        fields_to_update['departure_gate'] = api_data['departure_gate']
    if flight.arrival_gate != api_data['arrival_gate']:
        differences.append(("Arrival gate change",
                            f"Flight {flight.flight_number} from {flight.origin} to {flight.destination}, scheduled to arrive at {flight.scheduled_arrival}, has an arrival gate change from {flight.arrival_gate} to {api_data['arrival_gate']}"))
        fields_to_update['arrival_gate'] = api_data['arrival_gate']
    if flight.departure_terminal != api_data['departure_terminal']:
        differences.append(("Departure terminal change",
                            f"Flight {flight.flight_number} from {flight.origin} to {flight.destination}, scheduled to depart at {flight.scheduled_departure}, has a departure terminal change from {flight.departure_terminal} to {api_data['departure_terminal']}"))
        fields_to_update['departure_terminal'] = api_data['departure_terminal']
    if flight.arrival_terminal != api_data['arrival_terminal']:
        differences.append(("Arrival terminal change",
                            f"Flight {flight.flight_number} from {flight.origin} to {flight.destination}, scheduled to arrive at {flight.scheduled_arrival}, has an arrival terminal change from {flight.arrival_terminal} to {api_data['arrival_terminal']}"))
        fields_to_update['arrival_terminal'] = api_data['arrival_terminal']

    print(fields_to_update)
    print(differences)

    if differences:
        for diff_type, message in differences:
            await create_notification(flight, diff_type, message, session)
        await update_flight_details(flight, fields_to_update, session)

async def create_notification(flight, diff_type, message, session):
    notification = Notification(flight_id=flight.flight_id, type=diff_type, message=message, sent_at=datetime.now())
    session.add(notification)
    session.commit()
    # url = "http://127.0.0.1:8000/kafka/produce"
    # headers = {'Content-Type': 'application/json'}
    # payload = {
    #     "flight_id": str(flight.flight_id),
    #     "topic": 'notification',
    #     "message": message
    # }
    # response = requests.post(url, headers=headers, data=json.dumps(payload))
    # print(response.json())
    await producer.send_message('notification', '[' + str(flight.flight_id) + ']- ' + message)

async def update_flight_details(flight, updates, session):
    for field, value in updates.items():
        setattr(flight, field, value)
    setattr(flight,'last_updated', datetime.now())
    session.commit()

def convert_iso_to_standard(date_time_str):
    dt_object = datetime.fromisoformat(date_time_str.replace("Z", "+00:00"))
    formatted_date_time = dt_object.strftime("%Y-%m-%d %H:%M:%S")
    return formatted_date_time

def compare_datetimes(dt1, dt2_str):
    dt2 = convert_iso_to_standard(dt2_str)
    dt2 = datetime.strptime(dt2, "%Y-%m-%d %H:%M:%S")
    return dt1 != dt2

#
# schedule.every(2).seconds.do(check_flights_update)
#
# while True:
#     schedule.run_pending()
#     time.sleep(1)
