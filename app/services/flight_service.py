from sqlalchemy.orm import Session
from app.integrations.dummy_flight_api import search_flights
from app.models.flight import Flight
from app.repositories.flight_repository import save_flight
# from dateutil.parser import parse
from datetime import datetime

from sqlalchemy.orm import Session
from datetime import datetime
from app.integrations.dummy_flight_api import search_flights
from app.models.flight import Flight
from app.repositories.flight_repository import save_flight, get_flight_by_details, update_flight


def get_flight_details(flight_number, date, origin, destination, db: Session):
    # Fetch new flight data from the API
    dummy_flights = search_flights(flight_number, date, origin, destination)
    db_flights = []

    for flight_data in dummy_flights:
        # Ensure that the 'scheduled_departure' is a datetime object for filtering
        # if isinstance(flight_data['scheduled_departure'], str):
        #     flight_data['scheduled_departure'] = datetime.strptime(flight_data['scheduled_departure'], '%Y-%m-%dT%H:%M:%SZ')

        # Find the existing flight in the database
        existing_flight = get_flight_by_details(db, flight_number=flight_data['flight_number'],
                                                scheduled_departure=datetime.strptime(flight_data['scheduled_departure'], '%Y-%m-%dT%H:%M:%SZ'),
                                                origin=flight_data['origin'],
                                                destination=flight_data['destination'])

        if existing_flight:
            # Update the flight if there are changes
            is_updated = update_flight(db, existing_flight, flight_data)
            if is_updated:
                db.commit()
            db_flights.append(existing_flight.to_dict())  # Append the updated existing flight from DB
        else:
            # Create a new flight if it doesn't exist and save it to the DB
            new_flight = Flight(**flight_data)
            save_flight(db, new_flight)
            # flight_details_from_db = get_flight_by_details(db, flight_number=flight_data['flight_number'],
            #                                     scheduled_departure=flight_data['scheduled_departure'],
            #                                     origin=flight_data['origin'],
            #                                     destination=flight_data['destination'])
            db_flights.append(new_flight.to_dict())

    return db_flights


def list_all_flights(db: Session):
    return [flight.to_dict() for flight in db.query(Flight).all()]

#
# def get_flight_details(flight_number, date, origin, destination, db: Session):
#     dummy_flights = search_flights(flight_number, date, origin, destination)
#     db_flights = []
#
#     for flight_data in dummy_flights:
#         # Find the existing flight in the database
#         existing_flight = db.query(Flight).filter_by(
#             flight_number=flight_data['flight_number'],
#             scheduled_departure=datetime.strptime(flight_data['scheduled_departure'], '%Y-%m-%dT%H:%M:%SZ'),
#             origin=flight_data['origin'],
#             destination=flight_data['destination']
#         ).first()
#
#         # Check if the flight exists and update if there are changes
#         if existing_flight:
#             has_changed = False
#             # Check for changes in each field
#             for field in ['actual_departure', 'scheduled_arrival', 'actual_arrival', 'departure_gate', 'arrival_gate',
#                           'departure_terminal', 'arrival_terminal', 'status']:
#                 if getattr(existing_flight, field) != flight_data.get(field):
#                     setattr(existing_flight, field, flight_data.get(field))
#                     has_changed = True
#
#             if has_changed:
#                 db.commit()  # Commit changes if any field was updated
#
#             db_flights.append(existing_flight.to_dict())  # Add the updated existing flight to the return list
#         else:
#             # Create a new flight if it doesn't exist
#             flight = Flight(**flight_data)
#             db.add(flight)
#             db.commit()
#             db_flights.append(flight.to_dict())  # Add the new flight to the return list
#
#     return db_flights




def list_all_flights(db: Session):
    return db.query(Flight).all()
