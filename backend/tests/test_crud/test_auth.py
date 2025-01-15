import pytest
from sqlalchemy.orm import Session
from app.crud import auth
from app.schemas.auth import UserCreate, UserLogin

def test_create_user(db_session: Session):
    user_data = UserCreate(
        email="test@example.com",
        password="password123"
    )
    user = auth.create_user(db_session, user_data)
    assert user.email == "test@example.com"
    assert hasattr(user, "hashed_password")
    assert user.hashed_password != "password123"  # Password should be hashed

def test_get_user_by_email(db_session: Session):
    # Create a user first
    user_data = UserCreate(
        email="test@example.com",
        password="password123"
    )
    auth.create_user(db_session, user_data)
    
    # Try to get the user
    user = auth.get_user_by_email(db_session, "test@example.com")
    assert user is not None
    assert user.email == "test@example.com"

def test_authenticate_user_success(db_session: Session):
    # Create a user first
    user_data = UserCreate(
        email="test@example.com",
        password="password123"
    )
    auth.create_user(db_session, user_data)
    
    # Try to authenticate
    login_data = UserLogin(
        email="test@example.com",
        password="password123"
    )
    user = auth.authenticate_user(db_session, login_data)
    assert user is not None
    assert user.email == "test@example.com"

def test_authenticate_user_wrong_password(db_session: Session):
    # Create a user first
    user_data = UserCreate(
        email="test@example.com",
        password="password123"
    )
    auth.create_user(db_session, user_data)
    
    # Try to authenticate with wrong password
    login_data = UserLogin(
        email="test@example.com",
        password="wrongpassword"
    )
    user = auth.authenticate_user(db_session, login_data)
    assert user is None

def test_authenticate_user_nonexistent(db_session: Session):
    login_data = UserLogin(
        email="nonexistent@example.com",
        password="password123"
    )
    user = auth.authenticate_user(db_session, login_data)
    assert user is None 