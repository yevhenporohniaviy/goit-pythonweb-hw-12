from pydantic import BaseModel, EmailStr
from datetime import date
from typing import Optional

class ContactBase(BaseModel):
    """
    Base contact schema with common fields.
    
    This schema defines the basic structure for contact data validation.
    """
    first_name: str
    last_name: str
    email: EmailStr
    phone: str
    birthday: date | None = None
    additional_data: str | None = None

class ContactCreate(ContactBase):
    """
    Schema for creating a new contact.
    
    Inherits all fields from ContactBase for contact creation.
    """
    pass

class ContactUpdate(ContactBase):
    """
    Schema for updating an existing contact.
    
    All fields are optional to allow partial updates.
    """
    first_name: str | None = None
    last_name: str | None = None
    email: EmailStr | None = None
    phone: str | None = None
    birthday: date | None = None
    additional_data: str | None = None

class ContactResponse(ContactBase):
    """
    Schema for contact response data.
    
    Includes additional fields like id and user_id for API responses.
    """
    id: int
    user_id: int

    class Config:
        """Pydantic configuration for the ContactResponse schema."""
        from_attributes = True 