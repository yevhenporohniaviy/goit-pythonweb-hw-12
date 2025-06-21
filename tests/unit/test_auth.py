import pytest
from fastapi import HTTPException
from app.services.auth import (
    verify_password,
    get_password_hash,
    create_access_token,
)
from app.services.email import (
    create_password_reset_token,
    verify_password_reset_token,
)

def test_verify_password():
    """Test password verification."""
    password = "testpassword"
    hashed_password = get_password_hash(password)
    assert verify_password(password, hashed_password) is True
    assert verify_password("wrongpassword", hashed_password) is False

def test_create_access_token():
    """Test access token creation."""
    data = {"sub": "test@example.com"}
    token = create_access_token(data)
    assert isinstance(token, str)
    assert len(token) > 0

def test_create_password_reset_token():
    """Test password reset token creation."""
    email = "test@example.com"
    token = create_password_reset_token(email)
    assert isinstance(token, str)
    assert len(token) > 0

def test_verify_password_reset_token():
    """Test password reset token verification."""
    email = "test@example.com"
    token = create_password_reset_token(email)
    verified_email = verify_password_reset_token(token)
    assert verified_email == email

def test_verify_invalid_password_reset_token():
    """Test invalid password reset token verification."""
    with pytest.raises(HTTPException):
        verify_password_reset_token("invalid_token") 