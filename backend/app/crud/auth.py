from passlib.context import CryptContext
from sqlalchemy.orm import Session

import app.models as models
from app.schemas.auth import UserLogin, UserCreate

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def authenticate_user(db: Session, user_data: UserLogin):
    user = db.query(models.User).filter(models.User.email == user_data.email).first()
    if not user:
        return None
    if not pwd_context.verify(user_data.password, user.hashed_password):
        return None
    return user

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(db: Session, user: UserCreate):
    hashed_password = pwd_context.hash(user.password)
    db_user = models.User(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
