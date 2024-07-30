from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.subscription import SubscriptionCreate, Subscription, SubscriptionControllerModel
from app.services.subscription_service import subscribe_user, list_user_subscriptions, list_users_for_flight
from app.database import get_db
import uuid
from typing import List
from app.schemas.user import User
from app.services.auth_service import get_current_active_user


router = APIRouter()

@router.post("/", response_model=Subscription)
def subscribe_user_route(subscription: SubscriptionControllerModel, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    if not current_user:
        raise HTTPException(status_code=401, detail="User not authorized")
    user_id = current_user.user_id
    full_subscription_data = SubscriptionCreate(**subscription.dict(), user_id=user_id)
    return subscribe_user(full_subscription_data, db)


@router.get("/", response_model=List[Subscription])
def list_subscriptions_route(user_id: uuid.UUID, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    if not current_user:
        raise HTTPException(status_code=401, detail="User not authorized")
    return list_user_subscriptions(user_id, db)

@router.get("/flights/{flight_id}/subscribers")
def flight_subscribers(flight_id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    if not current_user:
        raise HTTPException(status_code=401, detail="User not authorized")
    try:
        return list_users_for_flight(flight_id, db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))