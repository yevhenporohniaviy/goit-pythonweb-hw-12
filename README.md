# Contacts API

A REST API for contact management built with FastAPI, PostgreSQL, and Redis.

## Features

- User authentication with JWT tokens
- **User roles and access control (user/admin)**
- Contact management (CRUD operations)
- Rate limiting with Redis
- **Redis caching for improved performance**
- **Secure password reset mechanism**
- **Environment-based configuration**
- **Full Docker containerization**
- Automatic API documentation
- Comprehensive test coverage (75%+)

## Quick Start

1. Clone the repository
2. Create a `.env` file with your configuration
3. Run with Docker:

```bash
docker-compose up -d
```

### Running Tests

````bash
# Run all tests
docker-compose exec web pytest

# Run tests with coverage
docker-compose exec web pytest --cov=app --cov-report=term-missing


### Building Documentation

```bash
# Using Docker
docker-compose -f docker-compose.docs.yml up docs

# Or using the script
./scripts/build_docs.sh
````

### Database Migrations

```bash
# Create a new migration
docker-compose exec web alembic revision --autogenerate -m "Description"

# Apply migrations
docker-compose exec web alembic upgrade head
```
