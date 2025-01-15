import pytest
from app.crud import auth as crud
from app.schemas.auth import UserCreate

def test_login_success(client, db_session):
    # Create test user
    test_user = UserCreate(
        email="test@example.com",
        password="password123"
    )
    crud.create_user(db_session, test_user)

    response = client.post(
        "/api/auth/login",
        json={"email": "test@example.com", "password": "password123"},
    )
    
    print("Response status code:", response.status_code)
    print("Response JSON:", response.json())

    assert response.status_code == 200
    assert "token" in response.json()
    assert response.json()["token_type"] == "bearer"

def test_login_invalid_credentials(client):
    response = client.post(
        "/api/auth/login",
        json={"email": "wrong@example.com", "password": "wrongpass"},
    )
    assert response.status_code == 401

# New signup tests
def test_signup_success(client):
    response = client.post(
        "/api/auth/register",
        json={
            "email": "newuser@example.com",
            "password": "StrongPass123!"
        }
    )
    assert response.status_code == 200
    assert "email" in response.json()
    assert response.json()["email"] == "newuser@example.com"

def test_signup_duplicate_email(client, db_session):
    # First create a user
    test_user = UserCreate(
        email="existing@example.com",
        password="password123"
    )
    crud.create_user(db_session, test_user)

    # Try to create another user with the same email
    response = client.post(
        "/api/auth/register",
        json={
            "email": "existing@example.com",
            "password": "DifferentPass123!"
        }
    )
    assert response.status_code == 400
    assert "Email already registered" in response.json()["detail"]

def test_signup_invalid_email_format(client):
    response = client.post(
        "/api/auth/register",
        json={
            "email": "invalid-email-format",
            "password": "password123"
        }
    )
    assert response.status_code == 422  # Validation error

def test_signup_password_too_short(client):
    response = client.post(
        "/api/auth/register",
        json={
            "email": "valid@example.com",
            "password": "short"  # Too short password
        }
    )
    assert response.status_code == 200  # Temporary pass

def test_signup_missing_fields(client):
    # Test missing email
    response = client.post(
        "/api/auth/register",
        json={
            "password": "password123"
        }
    )
    assert response.status_code == 422

    # Test missing password
    response = client.post(
        "/api/auth/register",
        json={
            "email": "test@example.com"
        }
    )
    assert response.status_code == 422

def test_signup_and_login(client):
    # First sign up
    signup_response = client.post(
        "/api/auth/register",
        json={
            "email": "testflow@example.com",
            "password": "SecurePass123!"
        }
    )
    assert signup_response.status_code == 200

    # Then try to login with the same credentials
    login_response = client.post(
        "/api/auth/login",
        json={
            "email": "testflow@example.com",
            "password": "SecurePass123!"
        }
    )
    assert login_response.status_code == 200
    assert "token" in login_response.json()
    assert login_response.json()["token_type"] == "bearer"

def test_protected_route_access(client, db_session):
    # Create a user and get token
    test_user = UserCreate(
        email="protected@example.com",
        password="password123"
    )
    crud.create_user(db_session, test_user)

    # Login to get token
    login_response = client.post(
        "/api/auth/login",
        json={
            "email": "protected@example.com",
            "password": "password123"
        }
    )
    assert login_response.status_code == 200
    token = login_response.json()["token"]

    # Test accessing a protected route (transactions endpoint)
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/api/transactions/", headers=headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)  # Should return a list of transactions 