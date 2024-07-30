from sqlalchemy.orm import Session
from app.models.flight import Flight
from app.schemas.flight import FlightBase
import uuid

def get_flight(db: Session, flight_id: uuid.UUID):
    return db.query(Flight).filter(Flight.flight_id == flight_id).first()

def save_flight(db: Session, flight_data: FlightBase):
    db.add(flight_data)
    db.commit()
    db.refresh(flight_data)
    return flight_data

def get_all_flights(db: Session):
    return db.query(Flight).all()

def get_flight_by_details(db, flight_number, scheduled_departure, origin, destination):
    return db.query(Flight).filter_by(
        flight_number=flight_number,
        scheduled_departure=scheduled_departure,
        origin=origin,
        destination=destination
    ).first()

def update_flight(db, flight, new_data ):
    changed = False
    for field in ['actual_departure', 'scheduled_arrival', 'actual_arrival',
                  'departure_gate', 'arrival_gate', 'departure_terminal',
                  'arrival_terminal', 'status']:
        if getattr(flight, field) != new_data.get(field):
            setattr(flight, field, new_data.get(field))
            changed = True
    return changed

