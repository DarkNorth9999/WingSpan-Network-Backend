from pydantic import BaseModel, EmailStr
import uuid
from typing import Optional

class UserBase(BaseModel):
    username: str
    email: str | None = None
    phone: str | None = None

class UserCreate(UserBase):
    password: str

class User(UserBase):
    user_id: str
    created_at: str
    last_login: str | None
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
    username: str

class TokenData(BaseModel):
    username: Optional[str] = None

    class Config:
        orm_mode = True
