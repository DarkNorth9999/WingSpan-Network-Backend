from sqlalchemy.orm import Session
from app.repositories.user_repository import get_user_by_username, create_user
from app.schemas.user import UserCreate
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password):
    return pwd_context.hash(password)

def register_user(user: UserCreate, db: Session):
    db_user = get_user_by_username(db, user.username)
    if db_user:
        raise ValueError("Username already registered")
    user.password = get_password_hash(user.password)
    return create_user(db, user)