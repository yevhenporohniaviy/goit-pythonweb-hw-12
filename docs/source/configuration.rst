Configuration and Environment Variables
=====================================

Цей документ описує конфігурацію додатку та управління конфіденційними даними.

Збереження конфіденційних даних
------------------------------

Всі конфіденційні дані та налаштування зберігаються у файлі `.env` та не включаються в кодову базу.

### Файл .env

Створіть файл `.env` в корені проекту з наступними змінними:

.. code-block:: env

    # Database Configuration
    POSTGRES_SERVER=localhost
    POSTGRES_USER=postgres
    POSTGRES_PASSWORD=postgres
    POSTGRES_DB=contacts

    # Security Configuration
    SECRET_KEY=your-super-secret-key-change-this-in-production
    ALGORITHM=HS256
    ACCESS_TOKEN_EXPIRE_MINUTES=30

    # Redis Configuration
    REDIS_HOST=localhost
    REDIS_PORT=6379
    REDIS_PASSWORD=your_redis_password
    REDIS_DB=0

    # CORS Configuration
    CORS_ORIGINS=["http://localhost:3000", "http://localhost:8000"]

    # Email Configuration (for password reset)
    SMTP_TLS=true
    SMTP_PORT=587
    SMTP_HOST=smtp.gmail.com
    SMTP_USER=your_email@gmail.com
    SMTP_PASSWORD=your_app_password
    EMAILS_FROM_EMAIL=your_email@gmail.com
    EMAILS_FROM_NAME=Contacts API
    EMAIL_RESET_TOKEN_EXPIRE_HOURS=48
    SERVER_HOST=http://localhost:8000

    # Application Configuration
    PROJECT_NAME=Contacts API
    VERSION=1.0.0
    API_V1_STR=/api/v1

### Файл .env.example

Проект включає файл `.env.example` з прикладом всіх необхідних змінних:

.. code-block:: bash

    cp .env.example .env
    # Відредагуйте .env з вашими реальними значеннями

### Безпека

- Файл `.env` додано до `.gitignore`
- Всі конфіденційні дані використовують змінні середовища
- Немає хардкоду паролів або ключів в коді

Змінні середовища
-----------------

### Database Configuration

POSTGRES_SERVER
~~~~~~~~~~~~~~~

Адреса сервера PostgreSQL.

**Тип:** string
**За замовчуванням:** localhost

POSTGRES_USER
~~~~~~~~~~~~~

Користувач бази даних PostgreSQL.

**Тип:** string
**За замовчуванням:** postgres

POSTGRES_PASSWORD
~~~~~~~~~~~~~~~~~

Пароль користувача бази даних PostgreSQL.

**Тип:** string
**За замовчуванням:** postgres

POSTGRES_DB
~~~~~~~~~~~

Назва бази даних PostgreSQL.

**Тип:** string
**За замовчуванням:** contacts

### Security Configuration

SECRET_KEY
~~~~~~~~~~

Секретний ключ для JWT токенів. **Обов'язково змініть в продакшені!**

**Тип:** string
**За замовчуванням:** your-secret-key-here

ALGORITHM
~~~~~~~~~

Алгоритм шифрування для JWT токенів.

**Тип:** string
**За замовчуванням:** HS256

ACCESS_TOKEN_EXPIRE_MINUTES
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Час життя access токена в хвилинах.

**Тип:** int
**За замовчуванням:** 30

### Redis Configuration

REDIS_HOST
~~~~~~~~~~

Адреса сервера Redis.

**Тип:** string
**За замовчуванням:** localhost

REDIS_PORT
~~~~~~~~~~

Порт сервера Redis.

**Тип:** int
**За замовчуванням:** 6379

REDIS_PASSWORD
~~~~~~~~~~~~~~

Пароль для Redis (опціонально).

**Тип:** string
**За замовчуванням:** ""

REDIS_DB
~~~~~~~~

Номер бази даних Redis.

**Тип:** int
**За замовчуванням:** 0

### CORS Configuration

CORS_ORIGINS
~~~~~~~~~~~~

Список дозволених origins для CORS.

**Тип:** List[str]
**За замовчуванням:** ["*"]

### Email Configuration

SMTP_TLS
~~~~~~~~

Використовувати TLS для SMTP.

**Тип:** bool
**За замовчуванням:** true

SMTP_PORT
~~~~~~~~~

Порт SMTP сервера.

**Тип:** int
**За замовчуванням:** 587

SMTP_HOST
~~~~~~~~~

Адреса SMTP сервера.

**Тип:** string
**За замовчуванням:** smtp.gmail.com

SMTP_USER
~~~~~~~~~

Користувач SMTP.

**Тип:** string
**За замовчуванням:** ""

SMTP_PASSWORD
~~~~~~~~~~~~~

Пароль SMTP (app password для Gmail).

**Тип:** string
**За замовчуванням:** ""

EMAILS_FROM_EMAIL
~~~~~~~~~~~~~~~~~

Email адреса відправника.

**Тип:** string
**За замовчуванням:** ""

EMAILS_FROM_NAME
~~~~~~~~~~~~~~~

Ім'я відправника.

**Тип:** string
**За замовчуванням:** ""

EMAIL_RESET_TOKEN_EXPIRE_HOURS
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Час життя токена скидання пароля в годинах.

**Тип:** int
**За замовчуванням:** 48

SERVER_HOST
~~~~~~~~~~~

Базовий URL сервера.

**Тип:** string
**За замовчуванням:** http://localhost:8000

### Application Configuration

PROJECT_NAME
~~~~~~~~~~~~

Назва проекту.

**Тип:** string
**За замовчуванням:** Contacts API

VERSION
~~~~~~~

Версія додатку.

**Тип:** string
**За замовчуванням:** 1.0.0

API_V1_STR
~~~~~~~~~~

Префікс API v1.

**Тип:** string
**За замовчуванням:** /api/v1

Контейнеризація
--------------

Проект повністю контейнеризований з використанням Docker Compose.

### Docker Compose

Файл `docker-compose.yml` включає всі необхідні сервіси:

.. code-block:: yaml

    version: "3.8"

    services:
      web:
        build: .
        ports:
          - "8000:8000"
        environment:
          - POSTGRES_SERVER=db
          - POSTGRES_USER=${POSTGRES_USER}
          - POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
          - POSTGRES_DB=${POSTGRES_DB}
          - SECRET_KEY=${SECRET_KEY}
          - ALGORITHM=HS256
          - ACCESS_TOKEN_EXPIRE_MINUTES=30
          - REDIS_HOST=redis
          - REDIS_PORT=6379
          - REDIS_PASSWORD=${REDIS_PASSWORD}
          - CORS_ORIGINS=["http://localhost:3000", "http://localhost:8000"]
        depends_on:
          - db
          - redis
        volumes:
          - .:/app
        networks:
          - app-network

      db:
        image: postgres:13
        environment:
          - POSTGRES_USER=${POSTGRES_USER}
          - POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
          - POSTGRES_DB=${POSTGRES_DB}
        ports:
          - "5434:5432"
        volumes:
          - postgres_data:/var/lib/postgresql/data
        networks:
          - app-network

      redis:
        image: redis:6
        command: redis-server --requirepass ${REDIS_PASSWORD}
        ports:
          - "6379:6379"
        networks:
          - app-network

    volumes:
      postgres_data:

    networks:
      app-network:
        driver: bridge

### Dockerfile

Файл `Dockerfile` для FastAPI додатку:

.. code-block:: dockerfile

    FROM python:3.10-slim

    WORKDIR /app

    # Install system dependencies
    RUN apt-get update && apt-get install -y \
        gcc \
        postgresql-client \
        && rm -rf /var/lib/apt/lists/*

    # Install Poetry
    RUN pip install poetry

    # Copy poetry configuration files
    COPY pyproject.toml poetry.lock* ./

    # Configure poetry to not use a virtual environment
    RUN poetry config virtualenvs.create false

    # Install dependencies
    RUN poetry install --no-interaction --no-ansi --no-root

    # Copy application code
    COPY . .

    # Create migrations directory if it doesn't exist
    RUN mkdir -p migrations/versions

    # Add current directory to PYTHONPATH
    ENV PYTHONPATH=/app

    # Expose port
    EXPOSE 8000

    # Command to run the application
    CMD ["sh", "-c", "alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 8000"]

### Запуск з Docker

1. Створіть файл `.env` з вашими налаштуваннями
2. Запустіть всі сервіси:

.. code-block:: bash

    docker-compose up -d

3. Перевірте статус сервісів:

.. code-block:: bash

    docker-compose ps

4. Перегляньте логи:

.. code-block:: bash

    docker-compose logs -f web

### Сервіси

**web** - FastAPI додаток
- Порт: 8000
- Залежить від: db, redis

**db** - PostgreSQL база даних
- Порт: 5434 (внутрішній 5432)
- Volume: postgres_data

**redis** - Redis кеш
- Порт: 6379
- Захищений паролем

### Мережі та Volumes

**app-network** - Bridge мережа для комунікації між контейнерами

**postgres_data** - Persistent volume для даних PostgreSQL

Налаштування для різних середовищ
---------------------------------

### Development

Використовуйте налаштування за замовчуванням з локальними сервісами.

### Production

1. Змініть `SECRET_KEY` на сильний випадковий ключ
2. Налаштуйте `CORS_ORIGINS` для ваших доменів
3. Використовуйте production бази даних
4. Налаштуйте SSL/TLS
5. Використовуйте production Redis з паролем

### Staging

Використовуйте окремі бази даних та Redis для тестування.

Перевірка конфігурації
---------------------

### Валідація змінних середовища

Pydantic автоматично валідує всі змінні середовища:

.. code-block:: python

    from app.core.config import settings
    
    # Перевірка налаштувань
    print(f"Database: {settings.POSTGRES_SERVER}")
    print(f"Redis: {settings.REDIS_HOST}:{settings.REDIS_PORT}")

### Тестування підключень

.. code-block:: bash

    # Тест підключення до бази даних
    docker-compose exec web python -c "
    from app.db.session import engine
    from sqlalchemy import text
    with engine.connect() as conn:
        result = conn.execute(text('SELECT 1'))
        print('Database connection: OK')
    "

    # Тест підключення до Redis
    docker-compose exec web python -c "
    import redis
    r = redis.Redis(host='redis', port=6379, password='your_redis_password')
    r.ping()
    print('Redis connection: OK')
    "

Безпека
-------

### Рекомендації

1. **Ніколи не комітьте `.env` файл**
2. Використовуйте сильні паролі
3. Обмежте доступ до баз даних
4. Регулярно оновлюйте залежності
5. Використовуйте HTTPS в продакшені
6. Налаштуйте firewall правила

### Перевірка безпеки

.. code-block:: bash

    # Перевірка відкритих портів
    docker-compose exec web netstat -tulpn
    
    # Перевірка змінних середовища
    docker-compose exec web env | grep -E "(PASSWORD|SECRET|KEY)" 