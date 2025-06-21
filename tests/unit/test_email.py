import pytest
from datetime import datetime, timedelta
from fastapi import HTTPException
from app.services.email import (
    create_password_reset_token,
    verify_password_reset_token,
    send_password_reset_email,
)
from app.core.config import settings

def test_create_password_reset_token():
    """Test creating a password reset token."""
    email = "test@example.com"
    token = create_password_reset_token(email)
    assert isinstance(token, str)
    assert len(token) > 0

def test_verify_password_reset_token():
    """Test verifying a valid password reset token."""
    email = "test@example.com"
    token = create_password_reset_token(email)
    verified_email = verify_password_reset_token(token)
    assert verified_email == email

def test_verify_invalid_password_reset_token():
    """Test verifying an invalid password reset token."""
    with pytest.raises(HTTPException) as exc_info:
        verify_password_reset_token("invalid_token")
    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == "Invalid token"

def test_verify_expired_password_reset_token():
    """Test verifying an expired password reset token."""
    # Create a token with very short expiration
    email = "test@example.com"
    delta = timedelta(seconds=1)  # 1 second expiration
    now = datetime.utcnow()
    expires = now + delta
    exp = expires.timestamp()
    
    import jwt
    token = jwt.encode(
        {"exp": exp, "nbf": now, "sub": email},
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )
    
    # Wait for token to expire
    import time
    time.sleep(2)
    
    with pytest.raises(HTTPException) as exc_info:
        verify_password_reset_token(token)
    assert exc_info.value.status_code == 400

def test_send_password_reset_email(caplog):
    """Test sending password reset email."""
    email = "test@example.com"
    send_password_reset_email(email)
    
    # Check that the function doesn't raise any exceptions
    # In a real application, this would send an actual email
    assert True

def test_password_reset_token_different_emails():
    """Test that tokens for different emails are different."""
    email1 = "user1@example.com"
    email2 = "user2@example.com"
    
    token1 = create_password_reset_token(email1)
    token2 = create_password_reset_token(email2)
    
    assert token1 != token2
    
    # Verify both tokens work correctly
    verified_email1 = verify_password_reset_token(token1)
    verified_email2 = verify_password_reset_token(token2)
    
    assert verified_email1 == email1
    assert verified_email2 == email2 