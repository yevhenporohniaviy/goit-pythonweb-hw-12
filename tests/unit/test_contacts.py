import pytest
from app.services.contacts import create_contact, get_contact, get_contacts, update_contact, delete_contact
from app.schemas.contact import ContactCreate, ContactUpdate

def test_create_contact(db_session, test_user):
    """Test creating a new contact."""
    contact_data = ContactCreate(
        first_name="John",
        last_name="Doe",
        email="john@example.com",
        phone="+1234567890"
    )
    contact = create_contact(db_session, contact_data, test_user.id)
    assert contact.first_name == "John"
    assert contact.last_name == "Doe"
    assert contact.email == "john@example.com"
    assert contact.phone == "+1234567890"
    assert contact.user_id == test_user.id

def test_get_contact(db_session, test_user):
    """Test retrieving a contact."""
    # Create a contact first
    contact_data = ContactCreate(
        first_name="John",
        last_name="Doe",
        email="john@example.com",
        phone="+1234567890"
    )
    created_contact = create_contact(db_session, contact_data, test_user.id)
    
    # Get the contact
    contact = get_contact(db_session, created_contact.id, test_user.id)
    assert contact is not None
    assert contact.id == created_contact.id
    assert contact.first_name == "John"

def test_get_contacts_with_pagination(db_session, test_user):
    """Test retrieving contacts with pagination."""
    # Create multiple contacts
    contacts_data = [
        ContactCreate(first_name="John", last_name="Doe", email="john@example.com", phone="+1234567890"),
        ContactCreate(first_name="Jane", last_name="Smith", email="jane@example.com", phone="+0987654321"),
        ContactCreate(first_name="Bob", last_name="Johnson", email="bob@example.com", phone="+1122334455"),
    ]
    
    for contact_data in contacts_data:
        create_contact(db_session, contact_data, test_user.id)
    
    # Test pagination
    contacts = get_contacts(db_session, test_user.id, skip=0, limit=2)
    assert len(contacts) == 2
    
    contacts = get_contacts(db_session, test_user.id, skip=2, limit=1)
    assert len(contacts) == 1
    assert contacts[0].first_name == "Bob"

def test_get_contacts_empty(db_session, test_user):
    """Test retrieving contacts when none exist."""
    contacts = get_contacts(db_session, test_user.id, skip=0, limit=10)
    assert len(contacts) == 0

def test_get_contact_not_found(db_session, test_user):
    """Test retrieving a non-existent contact."""
    contact = get_contact(db_session, 999, test_user.id)
    assert contact is None

def test_get_contact_wrong_user(db_session, test_user):
    """Test retrieving a contact with wrong user ID."""
    # Create a contact for test_user
    contact_data = ContactCreate(
        first_name="John",
        last_name="Doe",
        email="john@example.com",
        phone="+1234567890"
    )
    created_contact = create_contact(db_session, contact_data, test_user.id)
    
    # Try to get it with a different user ID
    contact = get_contact(db_session, created_contact.id, 999)
    assert contact is None

def test_update_contact(db_session, test_user):
    """Test updating a contact."""
    # Create a contact first
    contact_data = ContactCreate(
        first_name="John",
        last_name="Doe",
        email="john@example.com",
        phone="+1234567890"
    )
    created_contact = create_contact(db_session, contact_data, test_user.id)
    
    # Update the contact
    update_data = ContactUpdate(
        first_name="Jane",
        last_name="Doe",
        email="jane@example.com",
        phone="+0987654321"
    )
    updated_contact = update_contact(db_session, created_contact, update_data)
    assert updated_contact.first_name == "Jane"
    assert updated_contact.last_name == "Doe"
    assert updated_contact.email == "jane@example.com"
    assert updated_contact.phone == "+0987654321"

def test_update_contact_partial(db_session, test_user):
    """Test partial contact update."""
    # Create a contact first
    contact_data = ContactCreate(
        first_name="John",
        last_name="Doe",
        email="john@example.com",
        phone="+1234567890"
    )
    created_contact = create_contact(db_session, contact_data, test_user.id)
    
    # Update only first name
    update_data = ContactUpdate(first_name="Jane")
    updated_contact = update_contact(db_session, created_contact, update_data)
    assert updated_contact.first_name == "Jane"
    assert updated_contact.last_name == "Doe"  # Should remain unchanged
    assert updated_contact.email == "john@example.com"  # Should remain unchanged

def test_delete_contact(db_session, test_user):
    """Test deleting a contact."""
    # Create a contact first
    contact_data = ContactCreate(
        first_name="John",
        last_name="Doe",
        email="john@example.com",
        phone="+1234567890"
    )
    created_contact = create_contact(db_session, contact_data, test_user.id)
    
    # Delete the contact
    deleted_contact = delete_contact(db_session, created_contact.id)
    assert deleted_contact is not None
    
    # Verify the contact is deleted
    contact = get_contact(db_session, created_contact.id, test_user.id)
    assert contact is None 