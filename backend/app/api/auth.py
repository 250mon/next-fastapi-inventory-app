from datetime import datetime, timedelta, timezone
import os

import jwt
from fastapi import APIRouter, Depends, HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session
from pydantic import EmailStr

from app.crud import auth as crud
from app.schemas.auth import Token, TokenData, User, UserLogin, UserCreate
from app.database import get_db

router = APIRouter()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

security = HTTPBearer()

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Security(security),
    db: Session = Depends(get_db)
) -> User:
    try:
        token = credentials.credentials
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        exp: int = int(payload.get("exp"))
        user_id: int = payload.get("user_id")
        
        if email is None or user_id is None:
            raise HTTPException(status_code=401, detail="Invalid authentication token")
        
        if exp < int(datetime.now(timezone.utc).timestamp()):
            raise HTTPException(status_code=401, detail="Token has expired")
            
        token_data = TokenData(email=email, exp=exp, user_id=user_id)
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Could not validate credentials")
        
    user = crud.get_user_by_email(db, token_data.email)
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
        
    return user

@router.post("/login", response_model=Token)
def login(user_data: UserLogin, db: Session = Depends(get_db)):
    user = crud.authenticate_user(db, user_data)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    exp_timestamp = int(datetime.now(timezone.utc).timestamp()) + 1800
    token_data = {
        "sub": user.email,
        "exp": exp_timestamp,
        "user_id": user.id
    }
    token = jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITHM)

    return {"token": token, "token_type": "bearer"} 

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": int(expire.timestamp())})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt 

@router.post("/register", response_model=User)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    # Check if the user already exists
    existing_user = crud.get_user_by_email(db, user_data.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Create a new user
    user = crud.create_user(db, user_data)
    return user 