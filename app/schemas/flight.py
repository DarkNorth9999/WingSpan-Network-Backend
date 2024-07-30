from pydantic import BaseModel
import uuid
from datetime import datetime
from typing import Optional

class FlightBase(BaseModel):
    flight_number: str
    airline: str
    origin: str
    destination: str
    scheduled_departure: datetime
    scheduled_arrival: datetime
    status: str

class Flight(FlightBase):
    flight_id: uuid.UUID
    actual_departure: Optional[datetime] = None
    actual_arrival: Optional[datetime] = None
    departure_gate: Optional[str] = None
    arrival_gate: Optional[str] = None
    departure_terminal: Optional[str] = None
    arrival_terminal: Optional[str] = None
    last_updated: datetime
    subscription_count: int

    class Config:
        orm_mode = True
