from sqlalchemy.orm import Session
from app.repositories.notification_repository import get_notifications_by_user, create_notification,get_user_notifications
from app.schemas.notification import NotificationCreate
import uuid
def get_user_notifications(user_id: uuid.UUID, db: Session):
    return get_notifications_by_user(db, user_id)

def add_notification(notification: NotificationCreate, db: Session):
    return create_notification(db, notification)

def fetch_notifications_for_user(user_id, db: Session):
    notifications = get_user_notifications(user_id, db)
    # Convert to DTOs or perform any additional business logic here
    return [notification.to_dict() for notification in notifications]
