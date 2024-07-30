from pydantic import BaseModel
import uuid
from datetime import datetime

class NotificationBase(BaseModel):
    flight_id: uuid.UUID
    type: str
    message: str

class NotificationCreate(NotificationBase):
    pass

class Notification(NotificationBase):
    notification_id: uuid.UUID
    sent_at: datetime

    class Config:
        orm_mode = True
