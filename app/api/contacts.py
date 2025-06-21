from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_limiter.depends import RateLimiter
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.user import User
from app.schemas.contact import ContactCreate, ContactResponse, ContactUpdate
from app.services.auth import get_current_active_user
from app.services.contacts import (
    create_contact_with_cache,
    delete_contact_with_cache,
    get_contact_with_cache,
    get_contacts_with_cache,
    update_contact_with_cache,
)

router = APIRouter()


@router.post("/", response_model=ContactResponse, status_code=status.HTTP_201_CREATED)
async def create_new_contact(
    contact_in: ContactCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Create a new contact for the authenticated user.
    
    Args:
        contact_in (ContactCreate): Contact data to create
        db (Session): Database session
        current_user (User): Currently authenticated user
        
    Returns:
        ContactResponse: The created contact data
        
    Raises:
        HTTPException: If contact creation fails
    """
    return await create_contact_with_cache(db=db, contact=contact_in, user_id=current_user.id)


@router.get("/", response_model=List[ContactResponse])
async def read_contacts(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Retrieve a paginated list of contacts for the authenticated user.
    
    Args:
        skip (int): Number of records to skip (for pagination)
        limit (int): Maximum number of records to return
        db (Session): Database session
        current_user (User): Currently authenticated user
        
    Returns:
        List[ContactResponse]: List of contacts for the user
    """
    return await get_contacts_with_cache(db=db, user_id=current_user.id, skip=skip, limit=limit)


@router.get("/{contact_id}", response_model=ContactResponse)
async def read_contact(
    contact_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Get a specific contact by ID for the authenticated user.
    
    Args:
        contact_id (int): ID of the contact to retrieve
        db (Session): Database session
        current_user (User): Currently authenticated user
        
    Returns:
        ContactResponse: The contact data
        
    Raises:
        HTTPException: If contact is not found
    """
    contact = await get_contact_with_cache(db=db, contact_id=contact_id, user_id=current_user.id)
    if not contact:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Contact not found",
        )
    return contact


@router.put("/{contact_id}", response_model=ContactResponse)
async def update_contact_by_id(
    contact_id: int,
    contact_in: ContactUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Update a specific contact by ID for the authenticated user.
    
    Args:
        contact_id (int): ID of the contact to update
        contact_in (ContactUpdate): New contact data
        db (Session): Database session
        current_user (User): Currently authenticated user
        
    Returns:
        ContactResponse: The updated contact data
        
    Raises:
        HTTPException: If contact is not found
    """
    contact = await get_contact_with_cache(db=db, contact_id=contact_id, user_id=current_user.id)
    if not contact:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Contact not found",
        )
    return await update_contact_with_cache(db=db, contact=contact, contact_in=contact_in)


@router.delete("/{contact_id}", response_model=ContactResponse)
async def delete_contact_by_id(
    contact_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Delete a specific contact by ID for the authenticated user.
    
    Args:
        contact_id (int): ID of the contact to delete
        db (Session): Database session
        current_user (User): Currently authenticated user
        
    Returns:
        ContactResponse: The deleted contact data
        
    Raises:
        HTTPException: If contact is not found
    """
    contact = await get_contact_with_cache(db=db, contact_id=contact_id, user_id=current_user.id)
    if not contact:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Contact not found",
        )
    return await delete_contact_with_cache(db=db, contact_id=contact_id) 