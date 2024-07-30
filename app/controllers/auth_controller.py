from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate, User
from app.services.user_service import register_user
from app.database import get_db
from pydantic import ValidationError
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from app.services.auth_service import authenticate_user, create_access_token
from app.schemas.user import Token

router = APIRouter()

@router.post("/register")
def register_user_route(user: UserCreate, db: Session = Depends(get_db)):
    try:
        user = register_user(user, db)
        access_token_expires = timedelta(minutes=60)
        access_token = create_access_token(
            data={"sub": user.username}, expires_delta=access_token_expires
        )
        return {"access_token": access_token, "token_type": "bearer", "username": user.username}

    except ValidationError as ve:
        raise HTTPException(status_code=422, detail=ve.errors())
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))



# @router.post("/token", response_model=Token)
# async def login_for_access_token(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
#     user = authenticate_user(db, form_data.username, form_data.password)
#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Incorrect username or password",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
#     access_token_expires = timedelta(minutes=60)
#     access_token = create_access_token(
#         data={"sub": user.username}, expires_delta=access_token_expires
#     )
#     return {"access_token": access_token, "token_type": "bearer"}
