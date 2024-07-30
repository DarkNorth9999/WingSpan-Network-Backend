from sqlalchemy import Column, UUID, Boolean
from sqlalchemy.ext.declarative import declarative_base
import uuid

Base = declarative_base()

class Subscription(Base):
    __tablename__ = "subscriptions"
    subscription_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), nullable=False)
    flight_id = Column(UUID(as_uuid=True), nullable=False)
    email = Column(Boolean, default=False)
    phone_number = Column(Boolean, default=False)
