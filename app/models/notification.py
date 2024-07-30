from sqlalchemy import Column, String, TIMESTAMP, UUID
from sqlalchemy.ext.declarative import declarative_base
import uuid

Base = declarative_base()

class Notification(Base):
    __tablename__ = "notifications"
    notification_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    flight_id = Column(UUID(as_uuid=True), nullable=False)
    type = Column(String, nullable=False)
    message = Column(String, nullable=False)
    sent_at = Column(TIMESTAMP, nullable=False)
