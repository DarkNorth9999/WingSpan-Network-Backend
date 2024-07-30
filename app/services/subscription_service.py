from sqlalchemy.orm import Session
from app.repositories.subscription_repository import get_subscriptions_by_user, create_subscription, get_subscribed_users, get_subscription_by_user_and_flight
from app.schemas.subscription import SubscriptionCreate
import uuid

def subscribe_user(subscription: SubscriptionCreate, db: Session):
    # Check if the subscription already exists
    existing_subscription = get_subscription_by_user_and_flight(db, subscription.user_id, subscription.flight_id)
    if existing_subscription:
        # Update logic here if needed, e.g., update certain fields or toggle a status
        existing_subscription.email = subscription.email  # Example field
        existing_subscription.phone_number = subscription.phone_number  # Example field
        db.commit()
        return existing_subscription
    else:
        # Create new subscription if not existing
        return create_subscription(db, subscription)


def list_user_subscriptions(user_id: uuid.UUID, db: Session):
    return get_subscriptions_by_user(db, user_id)


def list_users_for_flight(flight_id, db: Session):
    users = get_subscribed_users(flight_id, db)
    # Additional logic to format or filter user data if needed
    return [{user.username, user.email, user.phone} for user in users]
