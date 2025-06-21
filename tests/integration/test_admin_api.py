"""
Integration tests for admin API endpoints.
"""

import pytest
from fastapi import status


def test_admin_dashboard_access(client, test_admin):
    """Test admin dashboard access."""
    # Login as admin
    login_data = {
        "username": test_admin.email,
        "password": "adminpassword"
    }
    response = client.post("/api/v1/auth/login", data=login_data)
    token = response.json()["access_token"]
    
    # Access admin dashboard
    response = client.get(
        "/api/v1/auth/admin",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "total_users" in data
    assert "admin_users" in data
    assert "regular_users" in data
    assert "message" in data


def test_admin_dashboard_denied_for_regular_user(client, test_user):
    """Test that regular users cannot access admin dashboard."""
    # Login as regular user
    login_data = {
        "username": test_user.email,
        "password": "testpassword"
    }
    response = client.post("/api/v1/auth/login", data=login_data)
    token = response.json()["access_token"]
    
    # Try to access admin dashboard
    response = client.get(
        "/api/v1/auth/admin",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_get_all_users_admin(client, test_admin, test_user):
    """Test getting all users as admin."""
    # Login as admin
    login_data = {
        "username": test_admin.email,
        "password": "adminpassword"
    }
    response = client.post("/api/v1/auth/login", data=login_data)
    token = response.json()["access_token"]
    
    # Get all users
    response = client.get(
        "/api/v1/auth/admin/users",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == status.HTTP_200_OK
    users = response.json()
    assert len(users) >= 2  # At least admin and test user


def test_get_users_by_role_admin(client, test_admin, test_user):
    """Test getting users filtered by role."""
    # Login as admin
    login_data = {
        "username": test_admin.email,
        "password": "adminpassword"
    }
    response = client.post("/api/v1/auth/login", data=login_data)
    token = response.json()["access_token"]
    
    # Get admin users
    response = client.get(
        "/api/v1/auth/admin/users?role=admin",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == status.HTTP_200_OK
    admin_users = response.json()
    assert len(admin_users) >= 1
    
    # Get regular users
    response = client.get(
        "/api/v1/auth/admin/users?role=user",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == status.HTTP_200_OK
    regular_users = response.json()
    assert len(regular_users) >= 1


def test_get_user_by_id_admin(client, test_admin, test_user):
    """Test getting specific user by ID as admin."""
    # Login as admin
    login_data = {
        "username": test_admin.email,
        "password": "adminpassword"
    }
    response = client.post("/api/v1/auth/login", data=login_data)
    token = response.json()["access_token"]
    
    # Get test user by ID
    response = client.get(
        f"/api/v1/auth/admin/users/{test_user.id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == status.HTTP_200_OK
    user_data = response.json()
    assert user_data["email"] == test_user.email
    assert user_data["role"] == test_user.role


def test_get_nonexistent_user_admin(client, test_admin):
    """Test getting non-existent user as admin."""
    # Login as admin
    login_data = {
        "username": test_admin.email,
        "password": "adminpassword"
    }
    response = client.post("/api/v1/auth/login", data=login_data)
    token = response.json()["access_token"]
    
    # Try to get non-existent user
    response = client.get(
        "/api/v1/auth/admin/users/99999",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_update_user_role_admin(client, test_admin, test_user):
    """Test updating user role as admin."""
    # Login as admin
    login_data = {
        "username": test_admin.email,
        "password": "adminpassword"
    }
    response = client.post("/api/v1/auth/login", data=login_data)
    token = response.json()["access_token"]
    
    # Update user role to admin
    update_data = {
        "role": "admin"
    }
    response = client.put(
        f"/api/v1/auth/admin/users/{test_user.id}",
        json=update_data,
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == status.HTTP_200_OK
    user_data = response.json()
    assert user_data["role"] == "admin"


def test_update_user_email_admin(client, test_admin, test_user):
    """Test updating user email as admin."""
    # Login as admin
    login_data = {
        "username": test_admin.email,
        "password": "adminpassword"
    }
    response = client.post("/api/v1/auth/login", data=login_data)
    token = response.json()["access_token"]
    
    # Update user email
    update_data = {
        "email": "updated@example.com"
    }
    response = client.put(
        f"/api/v1/auth/admin/users/{test_user.id}",
        json=update_data,
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == status.HTTP_200_OK
    user_data = response.json()
    assert user_data["email"] == "updated@example.com"


def test_delete_user_admin(client, test_admin, test_user):
    """Test deleting user as admin."""
    # Login as admin
    login_data = {
        "username": test_admin.email,
        "password": "adminpassword"
    }
    response = client.post("/api/v1/auth/login", data=login_data)
    token = response.json()["access_token"]
    
    # Delete user
    response = client.delete(
        f"/api/v1/auth/admin/users/{test_user.id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == status.HTTP_200_OK
    user_data = response.json()
    assert user_data["email"] == test_user.email


def test_delete_self_admin_denied(client, test_admin):
    """Test that admin cannot delete themselves."""
    # Login as admin
    login_data = {
        "username": test_admin.email,
        "password": "adminpassword"
    }
    response = client.post("/api/v1/auth/login", data=login_data)
    token = response.json()["access_token"]
    
    # Try to delete self
    response = client.delete(
        f"/api/v1/auth/admin/users/{test_admin.id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "Cannot delete yourself" in response.json()["detail"]


def test_regular_user_cannot_access_admin_endpoints(client, test_user):
    """Test that regular users cannot access any admin endpoints."""
    # Login as regular user
    login_data = {
        "username": test_user.email,
        "password": "testpassword"
    }
    response = client.post("/api/v1/auth/login", data=login_data)
    token = response.json()["access_token"]
    
    # Try to access admin endpoints
    admin_endpoints = [
        "/api/v1/auth/admin",
        "/api/v1/auth/admin/users",
        f"/api/v1/auth/admin/users/{test_user.id}",
    ]
    
    for endpoint in admin_endpoints:
        response = client.get(
            endpoint,
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN


def test_admin_endpoints_require_authentication(client):
    """Test that admin endpoints require authentication."""
    admin_endpoints = [
        "/api/v1/auth/admin",
        "/api/v1/auth/admin/users",
        "/api/v1/auth/admin/users/1",
    ]
    
    for endpoint in admin_endpoints:
        response = client.get(endpoint)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED 