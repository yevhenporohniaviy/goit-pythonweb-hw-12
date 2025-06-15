from pydantic import BaseModel, EmailStr
from datetime import date
from typing import Optional

class ContactBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone: str
    birthday: date | None = None
    additional_data: str | None = None

class ContactCreate(ContactBase):
    pass

class ContactUpdate(ContactBase):
    first_name: str | None = None
    last_name: str | None = None
    email: EmailStr | None = None
    phone: str | None = None
    birthday: date | None = None
    additional_data: str | None = None

class ContactResponse(ContactBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True 