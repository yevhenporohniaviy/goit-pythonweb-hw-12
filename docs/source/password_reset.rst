Password Reset Mechanism
========================

The Contacts API includes a secure password reset mechanism that allows users to reset their passwords via email.

## Overview

The password reset system provides:

- **Secure Token Generation**: JWT-based tokens with expiration
- **Email Notifications**: Password reset links sent via email
- **Token Verification**: Secure validation of reset tokens
- **Password Update**: Secure password hashing and storage
- **Security Features**: Token expiration, validation, and error handling

## API Endpoints

### Request Password Reset

**Endpoint**: `POST /api/v1/auth/password-reset-request`

**Request Body**:
```json
{
    "email": "user@example.com"
}
```

**Response**:
```json
{
    "message": "If the email exists, a password reset link has been sent"
}
```

**Description**: 
- Sends a password reset email if the user exists
- Always returns the same message for security (doesn't reveal if email exists)
- Generates a secure JWT token with expiration

### Reset Password

**Endpoint**: `POST /api/v1/auth/password-reset`

**Request Body**:
```json
{
    "token": "jwt_reset_token_here",
    "new_password": "new_secure_password"
}
```

**Response**:
```json
{
    "message": "Password updated successfully"
}
```

**Description**:
- Validates the reset token
- Updates the user's password with secure hashing
- Returns success message

## Security Features

### Token Security

- **JWT Tokens**: Uses JSON Web Tokens for secure token generation
- **Expiration**: Tokens expire after 48 hours (configurable)
- **Algorithm**: Uses HS256 algorithm with secret key
- **Validation**: Comprehensive token validation and error handling

### Password Security

- **Hashing**: Passwords are hashed using bcrypt
- **Validation**: Password strength validation (if implemented)
- **Storage**: Only hashed passwords are stored in database

### Email Security

- **No Information Disclosure**: API doesn't reveal if email exists
- **Secure Links**: Reset links include secure tokens
- **Expiration**: Links expire with token expiration

## Configuration

### Environment Variables

Configure password reset in your environment:

```env
# Email settings
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your_email@gmail.com
SMTP_PASSWORD=your_app_password
EMAILS_FROM_EMAIL=your_email@gmail.com
EMAILS_FROM_NAME=Contacts API

# Token settings
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
EMAIL_RESET_TOKEN_EXPIRE_HOURS=48

# Server settings
SERVER_HOST=http://localhost:8000
```

### Token Expiration

Default token expiration is 48 hours. You can adjust this in settings:

```python
EMAIL_RESET_TOKEN_EXPIRE_HOURS: int = 48
```

## Implementation Details

### Token Generation

```python
def create_password_reset_token(email: str) -> str:
    """Create a password reset token."""
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
```

### Token Verification

```python
def verify_password_reset_token(token: str) -> Optional[str]:
    """Verify password reset token."""
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
```

### Email Sending

```python
def send_password_reset_email(email_to: EmailStr) -> None:
    """Send password reset email."""
    token = create_password_reset_token(email_to)
    reset_link = f"{settings.SERVER_HOST}/reset-password?token={token}"
    
    # In production, send actual email here
    # For development, print the reset link
    print(f"Password reset link for {email_to}: {reset_link}")
```

## Usage Flow

### Complete Password Reset Process

1. **User requests password reset**:
   ```bash
   curl -X POST "http://localhost:8000/api/v1/auth/password-reset-request" \
        -H "Content-Type: application/json" \
        -d '{"email": "user@example.com"}'
   ```

2. **User receives email** with reset link:
   ```
   Password reset link: http://localhost:8000/reset-password?token=jwt_token_here
   ```

3. **User clicks link** and enters new password

4. **Frontend calls reset endpoint**:
   ```bash
   curl -X POST "http://localhost:8000/api/v1/auth/password-reset" \
        -H "Content-Type: application/json" \
        -d '{
          "token": "jwt_token_here",
          "new_password": "new_secure_password"
        }'
   ```

5. **User can login** with new password

## Error Handling

### Common Error Responses

**Invalid Token**:
```json
{
    "detail": "Invalid token"
}
```

**User Not Found**:
```json
{
    "detail": "User not found"
}
```

**Token Expired**:
```json
{
    "detail": "Invalid token"
}
```

## Best Practices

1. **Use Strong Passwords**: Implement password strength validation
2. **Rate Limiting**: Limit password reset requests per email
3. **Email Verification**: Ensure email addresses are verified
4. **Secure Tokens**: Use cryptographically secure token generation
5. **Token Expiration**: Set appropriate expiration times
6. **HTTPS**: Always use HTTPS in production
7. **Logging**: Log password reset attempts for security monitoring

## Frontend Integration

### React Example

```javascript
const requestPasswordReset = async (email) => {
  try {
    const response = await fetch('/api/v1/auth/password-reset-request', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ email }),
    });
    
    if (response.ok) {
      alert('If the email exists, a password reset link has been sent');
    }
  } catch (error) {
    console.error('Error requesting password reset:', error);
  }
};

const resetPassword = async (token, newPassword) => {
  try {
    const response = await fetch('/api/v1/auth/password-reset', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ token, new_password: newPassword }),
    });
    
    if (response.ok) {
      alert('Password updated successfully');
      // Redirect to login page
    }
  } catch (error) {
    console.error('Error resetting password:', error);
  }
};
```

## Testing

The password reset mechanism is thoroughly tested:

```bash
# Run password reset tests
pytest tests/unit/test_email.py -k "password_reset"
pytest tests/integration/test_auth_api.py -k "password_reset"
```

Test coverage includes:
- Token generation and verification
- Email sending functionality
- API endpoint testing
- Error handling scenarios
- Token expiration testing 