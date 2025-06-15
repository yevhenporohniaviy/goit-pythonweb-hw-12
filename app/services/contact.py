from sqlalchemy.orm import Session
from sqlalchemy import extract
from datetime import date, timedelta
from app.models.contact import Contact
from app.schemas.contact import ContactCreate, ContactUpdate

def get_contact(db: Session, contact_id: int):
    return db.query(Contact).filter(Contact.id == contact_id).first()

def get_contacts(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Contact).offset(skip).limit(limit).all()

def create_contact(db: Session, contact: ContactCreate):
    db_contact = Contact(**contact.model_dump())
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact

def update_contact(db: Session, contact_id: int, contact: ContactUpdate):
    db_contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if db_contact:
        update_data = contact.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_contact, key, value)
        db.commit()
        db.refresh(db_contact)
    return db_contact

def delete_contact(db: Session, contact_id: int):
    db_contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if db_contact:
        db.delete(db_contact)
        db.commit()
        return True
    return False

def search_contacts(db: Session, query: str):
    return db.query(Contact).filter(
        (Contact.first_name.ilike(f"%{query}%")) |
        (Contact.last_name.ilike(f"%{query}%")) |
        (Contact.email.ilike(f"%{query}%"))
    ).all()

def get_upcoming_birthdays(db: Session):
    today = date.today()
    end_date = today + timedelta(days=7)
    
    return db.query(Contact).filter(
        extract('month', Contact.birthday) == today.month,
        extract('day', Contact.birthday) >= today.day,
        extract('day', Contact.birthday) <= end_date.day
    ).all() 