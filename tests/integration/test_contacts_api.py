import pytest
from fastapi import status

def test_create_contact(client, test_user):
    """Test creating a contact through the API."""
    # Login first
    login_data = {
        "username": test_user.email,
        "password": "testpassword"
    }
    response = client.post("/api/v1/auth/login", data=login_data)
    assert response.status_code == status.HTTP_200_OK
    token = response.json()["access_token"]
    
    # Create contact
    contact_data = {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john@example.com",
        "phone": "+1234567890"
    }
    response = client.post(
        "/api/v1/contacts/",
        json=contact_data,
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["first_name"] == "John"
    assert data["last_name"] == "Doe"
    assert data["email"] == "john@example.com"
    assert data["phone"] == "+1234567890"

def test_get_contacts(client, test_user):
    """Test getting all contacts through the API."""
    # Login first
    login_data = {
        "username": test_user.email,
        "password": "testpassword"
    }
    response = client.post("/api/v1/auth/login", data=login_data)
    assert response.status_code == status.HTTP_200_OK
    token = response.json()["access_token"]
    
    # Get contacts
    response = client.get(
        "/api/v1/contacts/",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert isinstance(data, list)

def test_update_contact(client, test_user):
    """Test updating a contact through the API."""
    # Login first
    login_data = {
        "username": test_user.email,
        "password": "testpassword"
    }
    response = client.post("/api/v1/auth/login", data=login_data)
    assert response.status_code == status.HTTP_200_OK
    token = response.json()["access_token"]
    
    # Create contact first
    contact_data = {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john@example.com",
        "phone": "+1234567890"
    }
    response = client.post(
        "/api/v1/contacts/",
        json=contact_data,
        headers={"Authorization": f"Bearer {token}"}
    )
    contact_id = response.json()["id"]
    
    # Update contact
    update_data = {
        "first_name": "Jane",
        "last_name": "Doe",
        "email": "jane@example.com",
        "phone": "+0987654321"
    }
    response = client.put(
        f"/api/v1/contacts/{contact_id}",
        json=update_data,
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["first_name"] == "Jane"
    assert data["last_name"] == "Doe"
    assert data["email"] == "jane@example.com"
    assert data["phone"] == "+0987654321"

def test_delete_contact(client, test_user):
    """Test deleting a contact through the API."""
    # Login first
    login_data = {
        "username": test_user.email,
        "password": "testpassword"
    }
    response = client.post("/api/v1/auth/login", data=login_data)
    assert response.status_code == status.HTTP_200_OK
    token = response.json()["access_token"]
    
    # Create contact first
    contact_data = {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john@example.com",
        "phone": "+1234567890"
    }
    response = client.post(
        "/api/v1/contacts/",
        json=contact_data,
        headers={"Authorization": f"Bearer {token}"}
    )
    contact_id = response.json()["id"]
    
    # Delete contact
    response = client.delete(
        f"/api/v1/contacts/{contact_id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == status.HTTP_200_OK
    
    # Verify contact is deleted
    response = client.get(
        f"/api/v1/contacts/{contact_id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND 