from typing import List, Optional

from sqlalchemy.orm import Session

from app.models.contact import Contact
from app.schemas.contact import ContactCreate, ContactUpdate


def get_contact(db: Session, contact_id: int, user_id: int) -> Optional[Contact]:
    return db.query(Contact).filter(Contact.id == contact_id, Contact.user_id == user_id).first()


def get_contacts(
    db: Session, user_id: int, skip: int = 0, limit: int = 100
) -> List[Contact]:
    return (
        db.query(Contact)
        .filter(Contact.user_id == user_id)
        .offset(skip)
        .limit(limit)
        .all()
    )


def create_contact(db: Session, contact: ContactCreate, user_id: int) -> Contact:
    db_contact = Contact(**contact.model_dump(), user_id=user_id)
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact


def update_contact(
    db: Session, contact: Contact, contact_in: ContactUpdate
) -> Contact:
    for field, value in contact_in.model_dump(exclude_unset=True).items():
        setattr(contact, field, value)
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact


def delete_contact(db: Session, contact_id: int) -> Contact:
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    db.delete(contact)
    db.commit()
    return contact 