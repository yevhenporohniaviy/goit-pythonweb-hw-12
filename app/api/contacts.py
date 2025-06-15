from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_limiter.depends import RateLimiter
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.user import User
from app.schemas.contact import ContactCreate, ContactResponse, ContactUpdate
from app.services.auth import get_current_active_user
from app.services.contacts import (
    create_contact,
    delete_contact,
    get_contact,
    get_contacts,
    update_contact,
)

router = APIRouter()


@router.post("/", response_model=ContactResponse, status_code=status.HTTP_201_CREATED)
def create_new_contact(
    contact_in: ContactCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Create new contact.
    """
    return create_contact(db=db, contact=contact_in, user_id=current_user.id)


@router.get("/", response_model=List[ContactResponse])
def read_contacts(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Retrieve contacts.
    """
    return get_contacts(db=db, user_id=current_user.id, skip=skip, limit=limit)


@router.get("/{contact_id}", response_model=ContactResponse)
def read_contact(
    contact_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Get contact by ID.
    """
    contact = get_contact(db=db, contact_id=contact_id, user_id=current_user.id)
    if not contact:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Contact not found",
        )
    return contact


@router.put("/{contact_id}", response_model=ContactResponse)
def update_contact_by_id(
    contact_id: int,
    contact_in: ContactUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Update a contact.
    """
    contact = get_contact(db=db, contact_id=contact_id, user_id=current_user.id)
    if not contact:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Contact not found",
        )
    return update_contact(db=db, contact=contact, contact_in=contact_in)


@router.delete("/{contact_id}", response_model=ContactResponse)
def delete_contact_by_id(
    contact_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Delete a contact.
    """
    contact = get_contact(db=db, contact_id=contact_id, user_id=current_user.id)
    if not contact:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Contact not found",
        )
    return delete_contact(db=db, contact_id=contact_id) 