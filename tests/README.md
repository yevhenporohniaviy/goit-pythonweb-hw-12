# Testing

This directory contains all tests for the Contacts API application.

## Structure

```
tests/
├── conftest.py              # Pytest configuration and fixtures
├── unit/                    # Unit tests
│   ├── test_auth.py         # Authentication service tests
│   ├── test_contacts.py     # Contact service tests
│   ├── test_email.py        # Email service tests
│   ├── test_models.py       # Database model tests
│   └── test_schemas.py      # Pydantic schema tests
├── integration/             # Integration tests
│   ├── test_auth_api.py     # Authentication API tests
│   └── test_contacts_api.py # Contact API tests
└── test_coverage.py         # Coverage verification test
```

## Running Tests

### Using Docker

```bash
# Run all tests
docker-compose exec web pytest

# Run tests with coverage
docker-compose exec web pytest --cov=app --cov-report=term-missing

# Run tests with HTML coverage report
docker-compose exec web pytest --cov=app --cov-report=html

# Run specific test file
docker-compose exec web pytest tests/unit/test_contacts.py

# Run tests with verbose output
docker-compose exec web pytest -v
```

### Using the script

```bash
# Run tests with coverage check
./scripts/run_tests.sh
```

## Test Categories

### Unit Tests

- **Service Tests**: Test business logic in isolation
- **Model Tests**: Test database models and relationships
- **Schema Tests**: Test Pydantic validation schemas
- **Utility Tests**: Test helper functions and utilities

### Integration Tests

- **API Tests**: Test complete API endpoints
- **Database Tests**: Test database operations with real data
- **Authentication Tests**: Test JWT token flow

## Coverage Requirements

- **Minimum Coverage**: 75%
- **Coverage Tools**: pytest-cov
- **Reports**: Terminal and HTML reports available

## Test Fixtures

The `conftest.py` file provides common fixtures:

- `db_session`: Database session for tests
- `client`: FastAPI test client
- `test_user`: Sample user for testing
- `test_admin`: Sample admin user for testing

## Writing Tests

### Unit Test Example

```python
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
    assert contact.user_id == test_user.id
```

### Integration Test Example

```python
def test_create_contact_api(client, test_user):
    """Test creating a contact through the API."""
    # Login first
    login_data = {"username": test_user.email, "password": "testpassword"}
    response = client.post("/api/v1/auth/login", data=login_data)
    token = response.json()["access_token"]

    # Create contact
    contact_data = {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john@example.com",
        "phone": "+1234567890"
    }
    response = client.post(
        "/api/v1/contacts/",
        json=contact_data,
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 201
```

## Best Practices

1. **Test Naming**: Use descriptive test names that explain what is being tested
2. **Arrange-Act-Assert**: Structure tests with clear sections
3. **Isolation**: Each test should be independent and not rely on other tests
4. **Coverage**: Aim for high coverage but focus on critical paths
5. **Documentation**: Add docstrings to explain test purpose
6. **Fixtures**: Use fixtures for common setup and teardown

## Debugging Tests

```bash
# Run tests with debugger
docker-compose exec web pytest --pdb

# Run specific test with debugger
docker-compose exec web pytest tests/unit/test_contacts.py::test_create_contact --pdb

# Run tests with print statements
docker-compose exec web pytest -s
```
