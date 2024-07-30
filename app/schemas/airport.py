from pydantic import BaseModel

class AirportBase(BaseModel):
    code: str
    name: str

class AirportCreate(AirportBase):
    pass

class Airport(AirportBase):
    class Config:
        orm_mode = True
