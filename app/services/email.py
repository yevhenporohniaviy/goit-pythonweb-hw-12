from datetime import datetime, timedelta
from typing import Optional

from fastapi import HTTPException
from jose import jwt
from pydantic import EmailStr

from app.core.config import settings

def create_password_reset_token(email: str) -> str:
    """
    Create a password reset token.
    
    Args:
        email (str): User's email
        
    Returns:
        str: JWT token for password reset
    """
    delta = timedelta(hours=settings.EMAIL_RESET_TOKEN_EXPIRE_HOURS)
    now = datetime.utcnow()
    expires = now + delta
    exp = expires.timestamp()
    encoded_jwt = jwt.encode(
        {"exp": exp, "nbf": now, "sub": email},
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )
    return encoded_jwt

def verify_password_reset_token(token: str) -> Optional[str]:
    """
    Verify password reset token.
    
    Args:
        token (str): Password reset token
        
    Returns:
        Optional[str]: User's email if token is valid
        
    Raises:
        HTTPException: If token is invalid
    """
    try:
        decoded_token = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        return decoded_token["sub"]
    except jwt.JWTError:
        raise HTTPException(
            status_code=400,
            detail="Invalid token",
        )

def send_password_reset_email(email_to: EmailStr) -> None:
    """
    Send password reset email.
    
    Args:
        email_to (EmailStr): Recipient's email address
    """
    token = create_password_reset_token(email_to)
    reset_link = f"{settings.SERVER_HOST}/reset-password?token={token}"
    
    # In a real application, you would send an actual email here
    # For development, we'll just print the reset link
    print(f"Password reset link for {email_to}: {reset_link}") 