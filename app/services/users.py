"""
User service for managing user operations.
"""

from typing import List, Optional
from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate, UserAdminUpdate
from app.services.auth import get_password_hash


def create_user(db: Session, user_in: UserCreate) -> User:
    """
    Create a new user.
    
    Args:
        db (Session): Database session
        user_in (UserCreate): User creation data
        
    Returns:
        User: Created user
    """
    hashed_password = get_password_hash(user_in.password)
    db_user = User(
        email=user_in.email,
        hashed_password=hashed_password,
        role="user"  # Default role
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user_by_email(db: Session, email: str) -> Optional[User]:
    """
    Get user by email.
    
    Args:
        db (Session): Database session
        email (str): User's email
        
    Returns:
        Optional[User]: User if found, None otherwise
    """
    return db.query(User).filter(User.email == email).first()


def get_user_by_id(db: Session, user_id: int) -> Optional[User]:
    """
    Get user by ID.
    
    Args:
        db (Session): Database session
        user_id (int): User's ID
        
    Returns:
        Optional[User]: User if found, None otherwise
    """
    return db.query(User).filter(User.id == user_id).first()


def get_users(db: Session, skip: int = 0, limit: int = 100) -> List[User]:
    """
    Get list of users with pagination.
    
    Args:
        db (Session): Database session
        skip (int): Number of records to skip
        limit (int): Maximum number of records to return
        
    Returns:
        List[User]: List of users
    """
    return db.query(User).offset(skip).limit(limit).all()


def update_user(db: Session, user: User, user_in: UserUpdate) -> User:
    """
    Update user data.
    
    Args:
        db (Session): Database session
        user (User): User to update
        user_in (UserUpdate): Update data
        
    Returns:
        User: Updated user
    """
    update_data = user_in.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(user, field, value)
    
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def update_user_admin(db: Session, user: User, user_in: UserAdminUpdate) -> User:
    """
    Update user data by admin (can change role).
    
    Args:
        db (Session): Database session
        user (User): User to update
        user_in (UserAdminUpdate): Update data
        
    Returns:
        User: Updated user
    """
    update_data = user_in.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(user, field, value)
    
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def delete_user(db: Session, user: User) -> User:
    """
    Delete a user.
    
    Args:
        db (Session): Database session
        user (User): User to delete
        
    Returns:
        User: Deleted user
    """
    db.delete(user)
    db.commit()
    return user


def get_users_by_role(db: Session, role: str, skip: int = 0, limit: int = 100) -> List[User]:
    """
    Get users by role.
    
    Args:
        db (Session): Database session
        role (str): Role to filter by
        skip (int): Number of records to skip
        limit (int): Maximum number of records to return
        
    Returns:
        List[User]: List of users with specified role
    """
    return db.query(User).filter(User.role == role).offset(skip).limit(limit).all()


def count_users(db: Session) -> int:
    """
    Count total number of users.
    
    Args:
        db (Session): Database session
        
    Returns:
        int: Total number of users
    """
    return db.query(User).count()


def count_users_by_role(db: Session, role: str) -> int:
    """
    Count users by role.
    
    Args:
        db (Session): Database session
        role (str): Role to count
        
    Returns:
        int: Number of users with specified role
    """
    return db.query(User).filter(User.role == role).count() 