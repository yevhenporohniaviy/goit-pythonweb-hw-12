Development Guide
================

This guide is for developers working on the Contacts API project.

Setup
-----

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd goit-pythonweb-hw-12
   ```

2. **Start with Docker**
   ```bash
   docker-compose up -d
   ```

3. **Run migrations**
   ```bash
   docker-compose exec app alembic upgrade head
   ```

4. **Access the API**
   - API: http://localhost:8000
   - Documentation: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

Adding New Features
------------------

1. **Create database models** in ``app/models/``
2. **Create Pydantic schemas** in ``app/schemas/``
3. **Implement business logic** in ``app/services/``
4. **Create API endpoints** in ``app/api/``
5. **Add tests** in ``tests/``
6. **Update documentation** in ``docs/source/``

Code Style
----------

- Follow PEP 8 for Python code
- Use type hints for all function parameters and return values
- Add docstrings to all public functions and classes
- Use meaningful variable and function names

Testing
-------

Run tests with:
```bash
docker-compose exec app pytest
```

Run tests with coverage:
```bash
docker-compose exec app pytest --cov=app --cov-report=html
```

Documentation
------------

Build documentation:
```bash
docker-compose exec app sphinx-build -b html docs/source docs/build/html
```

When adding new modules:
1. Add docstrings to your code
2. Update the appropriate ``.rst`` file in ``docs/source/``
3. Rebuild the documentation

Database Migrations
------------------

Create a new migration:
```bash
docker-compose exec app alembic revision --autogenerate -m "Description"
```

Apply migrations:
```bash
docker-compose exec app alembic upgrade head
```

Environment Variables
--------------------

Create a ``.env`` file with the following variables:

```env
POSTGRES_SERVER=localhost
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=contacts
SECRET_KEY=your-secret-key-here
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_PASSWORD=
```

Deployment
----------

The application is containerized with Docker and can be deployed using:

```bash
docker-compose -f docker-compose.prod.yml up -d
```

Make sure to:
- Set proper environment variables for production
- Use a strong SECRET_KEY
- Configure proper database credentials
- Set up SSL/TLS certificates
- Configure proper CORS origins 