Architecture
===========

The Contacts API is built using a layered architecture pattern with the following components:

Application Structure
--------------------

::

    app/
    ├── api/           # API endpoints and routers
    ├── core/          # Core configuration and utilities
    ├── db/            # Database configuration and session management
    ├── models/        # SQLAlchemy database models
    ├── schemas/       # Pydantic data validation schemas
    ├── services/      # Business logic and data access layer
    └── main.py        # FastAPI application entry point

Technology Stack
---------------

- **Framework**: FastAPI - Modern, fast web framework for building APIs
- **Database**: PostgreSQL - Relational database
- **ORM**: SQLAlchemy - Python SQL toolkit and ORM
- **Authentication**: JWT tokens with python-jose
- **Password Hashing**: bcrypt with passlib
- **Rate Limiting**: Redis with fastapi-limiter
- **Documentation**: Sphinx with autodoc
- **Validation**: Pydantic - Data validation using Python type annotations

Database Design
---------------

The application uses two main tables:

**Users Table:**
- id (Primary Key)
- email (Unique)
- hashed_password
- is_active
- is_verified
- role

**Contacts Table:**
- id (Primary Key)
- first_name
- last_name
- email (Unique)
- phone
- birthday
- additional_data
- user_id (Foreign Key to Users)

Security Features
----------------

- JWT-based authentication
- Password hashing with bcrypt
- Rate limiting to prevent abuse
- CORS configuration
- Input validation with Pydantic
- SQL injection protection through SQLAlchemy ORM

API Design
----------

The API follows RESTful principles:

- **Authentication**: ``/api/v1/auth/*``
- **Contacts**: ``/api/v1/contacts/*``
- **OpenAPI**: Automatic documentation at ``/docs``
- **JSON**: All requests and responses use JSON format 