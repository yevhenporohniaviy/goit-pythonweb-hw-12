import pytest
from datetime import date
from pydantic import ValidationError
from app.schemas.contact import ContactBase, ContactCreate, ContactUpdate, ContactResponse
from app.schemas.user import UserCreate, UserResponse
from app.schemas.token import Token

def test_contact_base_valid():
    """Test ContactBase schema with valid data."""
    contact_data = {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john@example.com",
        "phone": "+1234567890",
        "birthday": date(1990, 1, 1),
        "additional_data": "Some notes"
    }
    contact = ContactBase(**contact_data)
    assert contact.first_name == "John"
    assert contact.last_name == "Doe"
    assert contact.email == "john@example.com"
    assert contact.phone == "+1234567890"
    assert contact.birthday == date(1990, 1, 1)
    assert contact.additional_data == "Some notes"

def test_contact_base_invalid_email():
    """Test ContactBase schema with invalid email."""
    contact_data = {
        "first_name": "John",
        "last_name": "Doe",
        "email": "invalid-email",
        "phone": "+1234567890"
    }
    with pytest.raises(ValidationError):
        ContactBase(**contact_data)

def test_contact_create():
    """Test ContactCreate schema."""
    contact_data = {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john@example.com",
        "phone": "+1234567890"
    }
    contact = ContactCreate(**contact_data)
    assert contact.first_name == "John"
    assert contact.last_name == "Doe"
    assert contact.email == "john@example.com"
    assert contact.phone == "+1234567890"

def test_contact_update_partial():
    """Test ContactUpdate schema with partial data."""
    contact_data = {
        "first_name": "Jane"
    }
    contact = ContactUpdate(**contact_data)
    assert contact.first_name == "Jane"
    assert contact.last_name is None
    assert contact.email is None
    assert contact.phone is None

def test_contact_response():
    """Test ContactResponse schema."""
    contact_data = {
        "id": 1,
        "first_name": "John",
        "last_name": "Doe",
        "email": "john@example.com",
        "phone": "+1234567890",
        "user_id": 1
    }
    contact = ContactResponse(**contact_data)
    assert contact.id == 1
    assert contact.first_name == "John"
    assert contact.user_id == 1

def test_user_create():
    """Test UserCreate schema."""
    user_data = {
        "email": "test@example.com",
        "password": "testpassword"
    }
    user = UserCreate(**user_data)
    assert user.email == "test@example.com"
    assert user.password == "testpassword"

def test_user_create_invalid_email():
    """Test UserCreate schema with invalid email."""
    user_data = {
        "email": "invalid-email",
        "password": "testpassword"
    }
    with pytest.raises(ValidationError):
        UserCreate(**user_data)

def test_user_response():
    """Test UserResponse schema."""
    user_data = {
        "id": 1,
        "email": "test@example.com",
        "is_active": True,
        "is_verified": True,
        "role": "user"
    }
    user = UserResponse(**user_data)
    assert user.id == 1
    assert user.email == "test@example.com"
    assert user.is_active is True
    assert user.is_verified is True
    assert user.role == "user"

def test_token():
    """Test Token schema."""
    token_data = {
        "access_token": "test_token_123",
        "token_type": "bearer"
    }
    token = Token(**token_data)
    assert token.access_token == "test_token_123"
    assert token.token_type == "bearer"

def test_contact_base_optional_fields():
    """Test ContactBase schema with optional fields."""
    contact_data = {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john@example.com",
        "phone": "+1234567890"
        # birthday and additional_data are optional
    }
    contact = ContactBase(**contact_data)
    assert contact.birthday is None
    assert contact.additional_data is None 