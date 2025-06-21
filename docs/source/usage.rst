Usage Guide
===========

This guide explains how to use the Contacts API.

Authentication
--------------

The API uses JWT tokens for authentication. To access protected endpoints:

1. Register a new user using ``POST /api/v1/auth/register``
2. Login using ``POST /api/v1/auth/login`` to get an access token
3. Include the token in the Authorization header: ``Bearer <token>``

Contact Management
-----------------

Contacts are user-specific. Each user can only access their own contacts.

**Create a contact:**
````
POST /api/v1/contacts/
{
    "first_name": "John",
    "last_name": "Doe",
    "email": "john@example.com",
    "phone": "+1234567890",
    "birthday": "1990-01-01",
    "additional_data": "Some notes"
}
````

**Get all contacts:**
````
GET /api/v1/contacts/?skip=0&limit=100
````

**Get a specific contact:**
````
GET /api/v1/contacts/{contact_id}
````

**Update a contact:**
````
PUT /api/v1/contacts/{contact_id}
{
    "first_name": "Jane",
    "email": "jane@example.com"
}
````

**Delete a contact:**
````
DELETE /api/v1/contacts/{contact_id}
````

Rate Limiting
------------

The API implements rate limiting to prevent abuse. Limits are applied per IP address.

Error Handling
-------------

The API returns appropriate HTTP status codes:

- 200: Success
- 201: Created
- 400: Bad Request
- 401: Unauthorized
- 404: Not Found
- 422: Validation Error
- 429: Too Many Requests 