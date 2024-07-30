from sqlalchemy.orm import Session
from app.models.notification import Notification
from app.models.subscription import Subscription
from app.schemas.notification import NotificationCreate
import uuid

def get_notifications_by_user(db: Session, user_id: uuid.UUID):
    return db.query(Notification).filter(Notification.user_id == user_id).all()

def create_notification(db: Session, notification: NotificationCreate):
    db_notification = Notification(**notification.dict())
    db.add(db_notification)
    db.commit()
    db.refresh(db_notification)
    return db_notification

def get_user_notifications(user_id, db: Session):
    return db.query(Notification).join(
        Subscription, Notification.flight_id == Subscription.flight_id
    ).filter(Subscription.user_id == user_id).all()