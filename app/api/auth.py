from datetime import timedelta
from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import create_access_token
from app.db.session import get_db
from app.models.user import User
from app.schemas.token import Token
from app.schemas.user import UserCreate, UserResponse, UserUpdate, UserAdminUpdate
from app.services.auth import (
    get_current_active_user,
    get_current_admin_user,
    get_password_hash,
    verify_password,
)
from app.services.email import send_password_reset_email, verify_password_reset_token
from app.services.users import (
    create_user,
    get_user_by_email,
    get_user_by_id,
    get_users,
    update_user,
    update_user_admin,
    delete_user,
    get_users_by_role,
    count_users,
    count_users_by_role,
)

router = APIRouter()


@router.post("/register", response_model=UserResponse)
def register_user(
    user_in: UserCreate,
    db: Session = Depends(get_db),
) -> Any:
    """
    Register a new user.
    
    Args:
        user_in (UserCreate): User registration data
        db (Session): Database session
        
    Returns:
        UserResponse: Created user data
    """
    user = get_user_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this email already exists in the system.",
        )
    user = create_user(db, user_in)
    return user


@router.post("/login", response_model=Token)
def login(
    db: Session = Depends(get_db),
    form_data: OAuth2PasswordRequestForm = Depends(),
) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests.
    
    Args:
        db (Session): Database session
        form_data (OAuth2PasswordRequestForm): Login form data
        
    Returns:
        Token: Access token
        
    Raises:
        HTTPException: If authentication fails
    """
    user = get_user_by_email(db, email=form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        "access_token": create_access_token(
            data={"sub": user.email}, expires_delta=access_token_expires
        ),
        "token_type": "bearer",
    }


@router.post("/password-reset-request")
def request_password_reset(
    email: str,
    db: Session = Depends(get_db),
) -> Any:
    """
    Request a password reset.
    
    Args:
        email (str): User's email
        db (Session): Database session
        
    Returns:
        dict: Success message
    """
    user = get_user_by_email(db, email=email)
    if user:
        send_password_reset_email(email_to=user.email)
    return {"message": "If the email exists, a password reset link has been sent"}


@router.post("/password-reset")
def reset_password(
    token: str,
    new_password: str,
    db: Session = Depends(get_db),
) -> Any:
    """
    Reset password using token.
    
    Args:
        token (str): Password reset token
        new_password (str): New password
        db (Session): Database session
        
    Returns:
        dict: Success message
        
    Raises:
        HTTPException: If token is invalid
    """
    try:
        email = verify_password_reset_token(token)
    except HTTPException:
        raise HTTPException(
            status_code=400,
            detail="Invalid token",
        )
    user = get_user_by_email(db, email=email)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )
    user.hashed_password = get_password_hash(new_password)
    db.add(user)
    db.commit()
    return {"message": "Password updated successfully"}


@router.get("/me", response_model=UserResponse)
def read_users_me(
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Get current user.
    
    Args:
        current_user (User): Current authenticated user
        
    Returns:
        UserResponse: Current user data
    """
    return current_user


# Admin endpoints
@router.get("/admin", response_model=dict)
def admin_dashboard(
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db),
) -> Any:
    """
    Admin dashboard with user statistics.
    
    Args:
        current_user (User): Current admin user
        db (Session): Database session
        
    Returns:
        dict: Dashboard statistics
    """
    total_users = count_users(db)
    admin_users = count_users_by_role(db, "admin")
    regular_users = count_users_by_role(db, "user")
    
    return {
        "total_users": total_users,
        "admin_users": admin_users,
        "regular_users": regular_users,
        "message": "Welcome to admin dashboard"
    }


@router.get("/admin/users", response_model=List[UserResponse])
def get_all_users(
    skip: int = 0,
    limit: int = 100,
    role: str = None,
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db),
) -> Any:
    """
    Get all users (admin only).
    
    Args:
        skip (int): Number of records to skip
        limit (int): Maximum number of records to return
        role (str): Filter by role
        current_user (User): Current admin user
        db (Session): Database session
        
    Returns:
        List[UserResponse]: List of users
    """
    if role:
        return get_users_by_role(db, role=role, skip=skip, limit=limit)
    return get_users(db, skip=skip, limit=limit)


@router.get("/admin/users/{user_id}", response_model=UserResponse)
def get_user_by_id_admin(
    user_id: int,
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db),
) -> Any:
    """
    Get user by ID (admin only).
    
    Args:
        user_id (int): User ID
        current_user (User): Current admin user
        db (Session): Database session
        
    Returns:
        UserResponse: User data
        
    Raises:
        HTTPException: If user not found
    """
    user = get_user_by_id(db, user_id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    return user


@router.put("/admin/users/{user_id}", response_model=UserResponse)
def update_user_admin_endpoint(
    user_id: int,
    user_in: UserAdminUpdate,
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db),
) -> Any:
    """
    Update user by admin (admin only).
    
    Args:
        user_id (int): User ID
        user_in (UserAdminUpdate): Update data
        current_user (User): Current admin user
        db (Session): Database session
        
    Returns:
        UserResponse: Updated user data
        
    Raises:
        HTTPException: If user not found
    """
    user = get_user_by_id(db, user_id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    return update_user_admin(db, user=user, user_in=user_in)


@router.delete("/admin/users/{user_id}", response_model=UserResponse)
def delete_user_admin(
    user_id: int,
    current_user: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db),
) -> Any:
    """
    Delete user (admin only).
    
    Args:
        user_id (int): User ID
        current_user (User): Current admin user
        db (Session): Database session
        
    Returns:
        UserResponse: Deleted user data
        
    Raises:
        HTTPException: If user not found or trying to delete self
    """
    if user_id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete yourself",
        )
    
    user = get_user_by_id(db, user_id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    return delete_user(db, user=user) 