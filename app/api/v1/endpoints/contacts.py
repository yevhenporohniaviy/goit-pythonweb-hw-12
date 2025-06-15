from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.api.deps import get_db
from app.schemas.contact import Contact, ContactCreate, ContactUpdate
from app.services import contact as contact_service

router = APIRouter()

@router.post("/", response_model=Contact)
def create_contact(contact: ContactCreate, db: Session = Depends(get_db)):
    return contact_service.create_contact(db=db, contact=contact)

@router.get("/", response_model=List[Contact])
def read_contacts(
    skip: int = 0,
    limit: int = 100,
    query: Optional[str] = None,
    db: Session = Depends(get_db)
):
    if query:
        return contact_service.search_contacts(db=db, query=query)
    return contact_service.get_contacts(db=db, skip=skip, limit=limit)

@router.get("/{contact_id}", response_model=Contact)
def read_contact(contact_id: int, db: Session = Depends(get_db)):
    db_contact = contact_service.get_contact(db=db, contact_id=contact_id)
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return db_contact

@router.put("/{contact_id}", response_model=Contact)
def update_contact(
    contact_id: int,
    contact: ContactUpdate,
    db: Session = Depends(get_db)
):
    db_contact = contact_service.update_contact(db=db, contact_id=contact_id, contact=contact)
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return db_contact

@router.delete("/{contact_id}")
def delete_contact(contact_id: int, db: Session = Depends(get_db)):
    success = contact_service.delete_contact(db=db, contact_id=contact_id)
    if not success:
        raise HTTPException(status_code=404, detail="Contact not found")
    return {"message": "Contact deleted successfully"}

@router.get("/birthdays/upcoming", response_model=List[Contact])
def get_upcoming_birthdays(db: Session = Depends(get_db)):
    return contact_service.get_upcoming_birthdays(db=db) 