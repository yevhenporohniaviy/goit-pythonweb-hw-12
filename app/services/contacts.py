from typing import List, Optional

from sqlalchemy.orm import Session

from app.models.contact import Contact
from app.schemas.contact import ContactCreate, ContactUpdate
from app.core.cache import cache


def get_contact(db: Session, contact_id: int, user_id: int) -> Optional[Contact]:
    """
    Retrieve a specific contact by ID for a given user.
    
    Args:
        db (Session): Database session
        contact_id (int): ID of the contact to retrieve
        user_id (int): ID of the user who owns the contact
        
    Returns:
        Optional[Contact]: The contact if found, None otherwise
    """
    return db.query(Contact).filter(Contact.id == contact_id, Contact.user_id == user_id).first()


async def get_contact_with_cache(db: Session, contact_id: int, user_id: int) -> Optional[Contact]:
    """
    Retrieve a specific contact by ID with caching.
    
    Args:
        db (Session): Database session
        contact_id (int): ID of the contact to retrieve
        user_id (int): ID of the user who owns the contact
        
    Returns:
        Optional[Contact]: The contact if found, None otherwise
    """
    # Try to get from cache first
    cached_contact = await cache.get_cached_contact(contact_id, user_id)
    if cached_contact:
        return Contact(**cached_contact)
    
    # Get from database
    contact = get_contact(db, contact_id, user_id)
    if contact:
        # Cache the contact
        contact_dict = {
            "id": contact.id,
            "first_name": contact.first_name,
            "last_name": contact.last_name,
            "email": contact.email,
            "phone": contact.phone,
            "birthday": contact.birthday.isoformat() if contact.birthday else None,
            "additional_data": contact.additional_data,
            "user_id": contact.user_id
        }
        await cache.cache_contact(contact_id, user_id, contact_dict)
    
    return contact


def get_contacts(
    db: Session, user_id: int, skip: int = 0, limit: int = 100
) -> List[Contact]:
    """
    Retrieve a list of contacts for a given user with pagination.
    
    Args:
        db (Session): Database session
        user_id (int): ID of the user whose contacts to retrieve
        skip (int): Number of records to skip (for pagination)
        limit (int): Maximum number of records to return
        
    Returns:
        List[Contact]: List of contacts for the user
    """
    return (
        db.query(Contact)
        .filter(Contact.user_id == user_id)
        .offset(skip)
        .limit(limit)
        .all()
    )


async def get_contacts_with_cache(
    db: Session, user_id: int, skip: int = 0, limit: int = 100
) -> List[Contact]:
    """
    Retrieve a list of contacts for a given user with caching.
    
    Args:
        db (Session): Database session
        user_id (int): ID of the user whose contacts to retrieve
        skip (int): Number of records to skip (for pagination)
        limit (int): Maximum number of records to return
        
    Returns:
        List[Contact]: List of contacts for the user
    """
    # For paginated results, we'll get from database and cache individual contacts
    contacts = get_contacts(db, user_id, skip, limit)
    
    # Cache individual contacts
    for contact in contacts:
        contact_dict = {
            "id": contact.id,
            "first_name": contact.first_name,
            "last_name": contact.last_name,
            "email": contact.email,
            "phone": contact.phone,
            "birthday": contact.birthday.isoformat() if contact.birthday else None,
            "additional_data": contact.additional_data,
            "user_id": contact.user_id
        }
        await cache.cache_contact(contact.id, user_id, contact_dict)
    
    return contacts


def create_contact(db: Session, contact: ContactCreate, user_id: int) -> Contact:
    """
    Create a new contact for a user.
    
    Args:
        db (Session): Database session
        contact (ContactCreate): Contact data to create
        user_id (int): ID of the user who will own the contact
        
    Returns:
        Contact: The created contact
    """
    db_contact = Contact(**contact.model_dump(), user_id=user_id)
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact


async def create_contact_with_cache(db: Session, contact: ContactCreate, user_id: int) -> Contact:
    """
    Create a new contact for a user with cache invalidation.
    
    Args:
        db (Session): Database session
        contact (ContactCreate): Contact data to create
        user_id (int): ID of the user who will own the contact
        
    Returns:
        Contact: The created contact
    """
    db_contact = create_contact(db, contact, user_id)
    
    # Invalidate user contacts cache
    await cache.invalidate_user_contacts_cache(user_id)
    
    return db_contact


def update_contact(
    db: Session, contact: Contact, contact_in: ContactUpdate
) -> Contact:
    """
    Update an existing contact with new data.
    
    Args:
        db (Session): Database session
        contact (Contact): The contact to update
        contact_in (ContactUpdate): New contact data
        
    Returns:
        Contact: The updated contact
    """
    for field, value in contact_in.model_dump(exclude_unset=True).items():
        setattr(contact, field, value)
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact


async def update_contact_with_cache(
    db: Session, contact: Contact, contact_in: ContactUpdate
) -> Contact:
    """
    Update an existing contact with new data and cache invalidation.
    
    Args:
        db (Session): Database session
        contact (Contact): The contact to update
        contact_in (ContactUpdate): New contact data
        
    Returns:
        Contact: The updated contact
    """
    updated_contact = update_contact(db, contact, contact_in)
    
    # Invalidate contact cache
    await cache.invalidate_contact_cache(contact.id, contact.user_id)
    # Invalidate user contacts cache
    await cache.invalidate_user_contacts_cache(contact.user_id)
    
    return updated_contact


def delete_contact(db: Session, contact_id: int) -> Contact:
    """
    Delete a contact by ID.
    
    Args:
        db (Session): Database session
        contact_id (int): ID of the contact to delete
        
    Returns:
        Contact: The deleted contact
    """
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    db.delete(contact)
    db.commit()
    return contact


async def delete_contact_with_cache(db: Session, contact_id: int) -> Contact:
    """
    Delete a contact by ID with cache invalidation.
    
    Args:
        db (Session): Database session
        contact_id (int): ID of the contact to delete
        
    Returns:
        Contact: The deleted contact
    """
    contact = delete_contact(db, contact_id)
    
    # Invalidate contact cache
    await cache.invalidate_contact_cache(contact_id, contact.user_id)
    # Invalidate user contacts cache
    await cache.invalidate_user_contacts_cache(contact.user_id)
    
    return contact 