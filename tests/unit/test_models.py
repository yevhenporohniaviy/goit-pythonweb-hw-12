import pytest
from datetime import date
from app.models.user import User
from app.models.contact import Contact
from app.core.security import get_password_hash

def test_user_model(db_session):
    """Test User model creation and attributes."""
    user = User(
        email="test@example.com",
        hashed_password=get_password_hash("testpassword"),
        is_active=True,
        is_verified=True,
        role="user"
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    
    assert user.id is not None
    assert user.email == "test@example.com"
    assert user.is_active is True
    assert user.is_verified is True
    assert user.role == "user"
    assert user.contacts == []

def test_contact_model(db_session, test_user):
    """Test Contact model creation and attributes."""
    contact = Contact(
        first_name="John",
        last_name="Doe",
        email="john@example.com",
        phone="+1234567890",
        birthday=date(1990, 1, 1),
        additional_data="Some notes",
        user_id=test_user.id
    )
    db_session.add(contact)
    db_session.commit()
    db_session.refresh(contact)
    
    assert contact.id is not None
    assert contact.first_name == "John"
    assert contact.last_name == "Doe"
    assert contact.email == "john@example.com"
    assert contact.phone == "+1234567890"
    assert contact.birthday == date(1990, 1, 1)
    assert contact.additional_data == "Some notes"
    assert contact.user_id == test_user.id
    assert contact.owner == test_user

def test_user_contacts_relationship(db_session, test_user):
    """Test User-Contact relationship."""
    # Create contacts for the user
    contact1 = Contact(
        first_name="John",
        last_name="Doe",
        email="john@example.com",
        phone="+1234567890",
        user_id=test_user.id
    )
    contact2 = Contact(
        first_name="Jane",
        last_name="Smith",
        email="jane@example.com",
        phone="+0987654321",
        user_id=test_user.id
    )
    
    db_session.add_all([contact1, contact2])
    db_session.commit()
    db_session.refresh(test_user)
    
    assert len(test_user.contacts) == 2
    assert test_user.contacts[0].first_name == "John"
    assert test_user.contacts[1].first_name == "Jane"

def test_contact_owner_relationship(db_session, test_user):
    """Test Contact-User relationship."""
    contact = Contact(
        first_name="John",
        last_name="Doe",
        email="john@example.com",
        phone="+1234567890",
        user_id=test_user.id
    )
    db_session.add(contact)
    db_session.commit()
    db_session.refresh(contact)
    
    assert contact.owner == test_user
    assert contact.owner.email == test_user.email

def test_contact_without_birthday(db_session, test_user):
    """Test Contact model without birthday."""
    contact = Contact(
        first_name="John",
        last_name="Doe",
        email="john@example.com",
        phone="+1234567890",
        user_id=test_user.id
    )
    db_session.add(contact)
    db_session.commit()
    db_session.refresh(contact)
    
    assert contact.birthday is None

def test_contact_without_additional_data(db_session, test_user):
    """Test Contact model without additional_data."""
    contact = Contact(
        first_name="John",
        last_name="Doe",
        email="john@example.com",
        phone="+1234567890",
        user_id=test_user.id
    )
    db_session.add(contact)
    db_session.commit()
    db_session.refresh(contact)
    
    assert contact.additional_data is None 