from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from app.services.flight_service import get_flight_details
from app.database import get_db
import json
from app.schemas.user import User
from app.services.auth_service import get_current_active_user

router = APIRouter()

@router.get("/search/")
def search_flight( flight_number: str = None, date_of_flight: str = None,
                  departure_airport: str = None, arrival_airport: str = None,
                  db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    try:
        if not current_user:
            raise HTTPException(status_code=401, detail="User not authorized")

        date_of_flight = datetime.strptime(date_of_flight, '%Y-%m-%dT%H:%M:%SZ')
        print(date_of_flight)
        flights = get_flight_details(flight_number, date_of_flight,
                                     departure_airport, arrival_airport, db)
        flights = flights[0]
        flights_json = json.dumps(flights)
        return flights_json
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
