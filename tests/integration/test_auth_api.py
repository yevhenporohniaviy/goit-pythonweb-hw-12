import pytest
from fastapi import status

def test_register_user(client):
    """Test user registration."""
    user_data = {
        "email": "newuser@example.com",
        "password": "testpassword"
    }
    response = client.post("/api/v1/auth/register", json=user_data)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["email"] == user_data["email"]
    assert "id" in data

def test_register_existing_user(client, test_user):
    """Test registering an existing user."""
    user_data = {
        "email": test_user.email,
        "password": "testpassword"
    }
    response = client.post("/api/v1/auth/register", json=user_data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST

def test_login(client, test_user):
    """Test user login."""
    login_data = {
        "username": test_user.email,
        "password": "testpassword"
    }
    response = client.post("/api/v1/auth/login", data=login_data)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_login_wrong_password(client, test_user):
    """Test login with wrong password."""
    login_data = {
        "username": test_user.email,
        "password": "wrongpassword"
    }
    response = client.post("/api/v1/auth/login", data=login_data)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

def test_password_reset_request(client, test_user):
    """Test password reset request."""
    response = client.post(
        "/api/v1/auth/password-reset-request",
        json={"email": test_user.email}
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "message" in data

def test_get_current_user(client, test_user):
    """Test getting current user."""
    # Login first
    login_data = {
        "username": test_user.email,
        "password": "testpassword"
    }
    response = client.post("/api/v1/auth/login", data=login_data)
    token = response.json()["access_token"]
    
    # Get current user
    response = client.get(
        "/api/v1/auth/me",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["email"] == test_user.email

def test_admin_access(client, test_admin):
    """Test admin access."""
    # Login as admin
    login_data = {
        "username": test_admin.email,
        "password": "adminpassword"
    }
    response = client.post("/api/v1/auth/login", data=login_data)
    token = response.json()["access_token"]
    
    # Try to access admin endpoint
    response = client.get(
        "/api/v1/auth/admin",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == status.HTTP_200_OK 