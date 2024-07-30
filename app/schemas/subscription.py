from pydantic import BaseModel
import uuid

class SubscriptionBase(BaseModel):
    user_id: uuid.UUID
    flight_id: uuid.UUID

class SubscriptionCreate(SubscriptionBase):
    email: bool
    phone_number: bool


class SubscriptionControllerModel(BaseModel):
    flight_id: uuid.UUID
    email: bool
    phone_number: bool




class Subscription(SubscriptionBase):
    subscription_id: uuid.UUID

    class Config:
        orm_mode = True
