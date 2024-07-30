from sqlalchemy import Column, String, TIMESTAMP, Integer, UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from datetime import datetime
from pydantic import BaseModel
import uuid

class FlightSearchRequest(BaseModel):
    flight_number: str
    date_of_flight: str
    departure_airport: str
    arrival_airport: str


Base = declarative_base()


class Flight(Base):
    __tablename__ = "flights"
    flight_id = Column(UUID(as_uuid=True), primary_key=True, server_default=func.uuid_generate_v4())
    flight_number = Column(String, nullable=False)
    airline = Column(String, nullable=False)
    origin = Column(String, nullable=False)
    destination = Column(String, nullable=False)
    scheduled_departure = Column(TIMESTAMP, nullable=False)
    actual_departure = Column(TIMESTAMP)
    scheduled_arrival = Column(TIMESTAMP, nullable=False)
    actual_arrival = Column(TIMESTAMP)
    departure_gate = Column(String)
    arrival_gate = Column(String)
    departure_terminal = Column(String)
    arrival_terminal = Column(String)
    status = Column(String, nullable=False)
    last_updated = Column(TIMESTAMP, nullable=False, server_default=func.current_timestamp(),
                          server_onupdate=func.current_timestamp())
    subscription_count = Column(Integer, default=0)



    def to_dict(self):
        return {
            "flight_id": str(self.flight_id),
            "flight_number": self.flight_number,
            "airline": self.airline,
            "origin": self.origin,
            "destination": self.destination,
            "scheduled_departure": self.scheduled_departure.isoformat() if isinstance(self.scheduled_departure,
                                                                                      datetime) else None,
            "actual_departure": self.actual_departure.isoformat() if isinstance(self.actual_departure,
                                                                                datetime) else None,
            "scheduled_arrival": self.scheduled_arrival.isoformat() if isinstance(self.scheduled_arrival,
                                                                                  datetime) else None,
            "actual_arrival": self.actual_arrival.isoformat() if isinstance(self.actual_arrival,
                                                                            datetime) else None,
            "departure_gate": self.departure_gate,
            "arrival_gate": self.arrival_gate,
            "departure_terminal": self.departure_terminal,
            "arrival_terminal": self.arrival_terminal,
            "status": self.status,
            "last_updated": self.last_updated.isoformat() if isinstance(self.last_updated, datetime) else None,
            "subscription_count": self.subscription_count
        }
    def to_dict_from_api(self):
        return {
            "flight_id": str(self.flight_id),
            "flight_number": self.flight_number,
            "airline": self.airline,
            "origin": self.origin,
            "destination": self.destination,
            "scheduled_departure": self.scheduled_departure,  # Assuming it's already a string
            "actual_departure": self.actual_departure,  # Assuming it's already a string
            "scheduled_arrival": self.scheduled_arrival,  # Assuming it's already a string
            "actual_arrival": self.actual_arrival,  # Assuming it's already a string
            "departure_gate": self.departure_gate,
            "arrival_gate": self.arrival_gate,
            "departure_terminal": self.departure_terminal,
            "arrival_terminal": self.arrival_terminal,
            "status": self.status,
            "last_updated": self.last_updated,  # Assuming it's already a string
            "subscription_count": self.subscription_count
        }
