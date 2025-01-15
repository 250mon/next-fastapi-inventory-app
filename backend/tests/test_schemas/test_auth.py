import pytest
from pydantic import ValidationError
from app.schemas.auth import UserCreate, UserLogin, Token, TokenData

def test_user_create_valid():
    user_data = {
        "email": "test@example.com",
        "password": "password123"
    }
    user = UserCreate(**user_data)
    assert user.email == "test@example.com"
    assert user.password == "password123"

def test_user_create_invalid_email():
    with pytest.raises(ValidationError):
        UserCreate(
            email="invalid_email",  # Invalid email format
            password="password123"
        )

def test_user_login_valid():
    login_data = {
        "email": "test@example.com",
        "password": "password123"
    }
    login = UserLogin(**login_data)
    assert login.email == "test@example.com"
    assert login.password == "password123"

def test_token_valid():
    token_data = {
        "token": "some.jwt.token",
        "token_type": "bearer"
    }
    token = Token(**token_data)
    assert token.token == "some.jwt.token"
    assert token.token_type == "bearer"

def test_token_data_valid():
    data = {
        "email": "test@example.com",
        "exp": 1234567890,
        "user_id": 1
    }
    token_data = TokenData(**data)
    assert token_data.email == "test@example.com"
    assert token_data.exp == 1234567890 
    assert token_data.user_id == 1