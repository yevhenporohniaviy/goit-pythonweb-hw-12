"""
Unit tests for user roles and permissions.
"""

import pytest
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.user import User
from app.services.auth import get_current_admin_user, get_current_active_user
from app.services.users import (
    create_user,
    get_user_by_email,
    update_user_admin,
    get_users_by_role,
    count_users_by_role
)
from app.schemas.user import UserCreate, UserAdminUpdate


def test_user_creation_with_default_role(db_session: Session):
    """Test that new users are created with 'user' role by default."""
    user_data = UserCreate(
        email="test@example.com",
        password="testpassword"
    )
    
    user = create_user(db_session, user_data)
    
    assert user.role == "user"
    assert user.email == "test@example.com"
    assert user.is_active is True


def test_admin_user_creation(db_session: Session):
    """Test creating an admin user."""
    user_data = UserCreate(
        email="admin@example.com",
        password="adminpassword"
    )
    
    user = create_user(db_session, user_data)
    # Manually set role to admin for testing
    user.role = "admin"
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    
    assert user.role == "admin"


def test_get_users_by_role(db_session: Session):
    """Test filtering users by role."""
    # Create regular users
    for i in range(3):
        user_data = UserCreate(
            email=f"user{i}@example.com",
            password="password"
        )
        create_user(db_session, user_data)
    
    # Create admin users
    for i in range(2):
        user_data = UserCreate(
            email=f"admin{i}@example.com",
            password="password"
        )
        user = create_user(db_session, user_data)
        user.role = "admin"
        db_session.add(user)
    
    db_session.commit()
    
    # Test filtering
    regular_users = get_users_by_role(db_session, "user")
    admin_users = get_users_by_role(db_session, "admin")
    
    assert len(regular_users) == 3
    assert len(admin_users) == 2
    
    for user in regular_users:
        assert user.role == "user"
    
    for user in admin_users:
        assert user.role == "admin"


def test_count_users_by_role(db_session: Session):
    """Test counting users by role."""
    # Create users
    for i in range(5):
        user_data = UserCreate(
            email=f"user{i}@example.com",
            password="password"
        )
        create_user(db_session, user_data)
    
    # Create admin
    user_data = UserCreate(
        email="admin@example.com",
        password="password"
    )
    user = create_user(db_session, user_data)
    user.role = "admin"
    db_session.add(user)
    db_session.commit()
    
    # Test counting
    user_count = count_users_by_role(db_session, "user")
    admin_count = count_users_by_role(db_session, "admin")
    
    assert user_count == 5
    assert admin_count == 1


def test_update_user_role_by_admin(db_session: Session):
    """Test updating user role by admin."""
    # Create regular user
    user_data = UserCreate(
        email="user@example.com",
        password="password"
    )
    user = create_user(db_session, user_data)
    
    # Update role to admin
    update_data = UserAdminUpdate(role="admin")
    updated_user = update_user_admin(db_session, user, update_data)
    
    assert updated_user.role == "admin"


def test_admin_permission_check(db_session: Session):
    """Test admin permission check function."""
    # Create admin user
    user_data = UserCreate(
        email="admin@example.com",
        password="password"
    )
    user = create_user(db_session, user_data)
    user.role = "admin"
    db_session.add(user)
    db_session.commit()
    
    # Test admin access
    admin_user = get_current_admin_user(user)
    assert admin_user.role == "admin"
    assert admin_user.email == "admin@example.com"


def test_non_admin_permission_denied(db_session: Session):
    """Test that non-admin users are denied admin access."""
    # Create regular user
    user_data = UserCreate(
        email="user@example.com",
        password="password"
    )
    user = create_user(db_session, user_data)
    
    # Test admin access denial
    with pytest.raises(HTTPException) as exc_info:
        get_current_admin_user(user)
    
    assert exc_info.value.status_code == 403
    assert "doesn't have enough privileges" in exc_info.value.detail


def test_inactive_user_access_denied(db_session: Session):
    """Test that inactive users are denied access."""
    # Create inactive user
    user_data = UserCreate(
        email="inactive@example.com",
        password="password"
    )
    user = create_user(db_session, user_data)
    user.is_active = False
    db_session.add(user)
    db_session.commit()
    
    # Test access denial
    with pytest.raises(HTTPException) as exc_info:
        get_current_active_user(user)
    
    assert exc_info.value.status_code == 400
    assert "Inactive user" in exc_info.value.detail


def test_user_role_validation(db_session: Session):
    """Test user role validation."""
    # Create user with invalid role
    user_data = UserCreate(
        email="test@example.com",
        password="password"
    )
    user = create_user(db_session, user_data)
    user.role = "invalid_role"
    db_session.add(user)
    db_session.commit()
    
    # Test that invalid role is not accepted for admin access
    with pytest.raises(HTTPException) as exc_info:
        get_current_admin_user(user)
    
    assert exc_info.value.status_code == 403 