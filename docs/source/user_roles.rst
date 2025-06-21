User Roles and Access Control
============================

Система ролей користувачів забезпечує контроль доступу до різних функцій додатку на основі ролей користувачів.

Ролі користувачів
----------------

Додаток підтримує дві основні ролі:

- **user** - звичайний користувач (за замовчуванням)
- **admin** - адміністратор з розширеними правами

Модель користувача
-----------------

.. code-block:: python

    class User(Base):
        __tablename__ = "users"
        
        id = Column(Integer, primary_key=True, index=True)
        email = Column(String, unique=True, index=True, nullable=False)
        hashed_password = Column(String, nullable=False)
        is_active = Column(Boolean, default=True)
        is_verified = Column(Boolean, default=False)
        role = Column(String, default="user")  # 'user' або 'admin'
        contacts = relationship("Contact", back_populates="owner")

Перевірка прав доступу
---------------------

Система використовує dependency injection для перевірки прав доступу:

.. code-block:: python

    from app.services.auth import get_current_active_user, get_current_admin_user

    # Для звичайних користувачів
    @router.get("/me")
    def read_users_me(current_user: User = Depends(get_current_active_user)):
        return current_user

    # Для адміністраторів
    @router.get("/admin")
    def admin_dashboard(current_user: User = Depends(get_current_admin_user)):
        return {"message": "Admin dashboard"}

Функції перевірки прав
---------------------

get_current_active_user()
~~~~~~~~~~~~~~~~~~~~~~~~~

Перевіряє, чи користувач автентифікований та активний.

.. code-block:: python

    def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
        if not current_user.is_active:
            raise HTTPException(status_code=400, detail="Inactive user")
        return current_user

get_current_admin_user()
~~~~~~~~~~~~~~~~~~~~~~~~

Перевіряє, чи користувач є адміністратором.

.. code-block:: python

    def get_current_admin_user(current_user: User = Depends(get_current_user)) -> User:
        if current_user.role != "admin":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="The user doesn't have enough privileges"
            )
        return current_user

Адміністративні ендпоінти
------------------------

Адміністратори мають доступ до спеціальних ендпоінтів для керування користувачами:

GET /api/v1/auth/admin
~~~~~~~~~~~~~~~~~~~~~~

Адміністративна панель зі статистикою користувачів.

**Відповідь:**
.. code-block:: json

    {
        "total_users": 10,
        "admin_users": 2,
        "regular_users": 8,
        "message": "Welcome to admin dashboard"
    }

GET /api/v1/auth/admin/users
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Отримання списку всіх користувачів з можливістю фільтрації за роллю.

**Параметри:**
- ``skip`` (int): Кількість записів для пропуску
- ``limit`` (int): Максимальна кількість записів
- ``role`` (str): Фільтр за роллю ('user' або 'admin')

GET /api/v1/auth/admin/users/{user_id}
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Отримання інформації про конкретного користувача.

PUT /api/v1/auth/admin/users/{user_id}
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Оновлення даних користувача (включаючи роль).

**Тіло запиту:**
.. code-block:: json

    {
        "email": "newemail@example.com",
        "is_active": true,
        "is_verified": true,
        "role": "admin"
    }

DELETE /api/v1/auth/admin/users/{user_id}
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Видалення користувача (адміністратор не може видалити себе).

Схеми для ролей
---------------

UserResponse
~~~~~~~~~~~~

.. code-block:: python

    class UserResponse(UserBase):
        id: int
        is_active: bool
        is_verified: bool
        role: str

UserUpdate
~~~~~~~~~~

.. code-block:: python

    class UserUpdate(BaseModel):
        email: Optional[EmailStr] = None
        is_active: Optional[bool] = None
        is_verified: Optional[bool] = None
        role: Optional[str] = None

UserAdminUpdate
~~~~~~~~~~~~~~~

.. code-block:: python

    class UserAdminUpdate(BaseModel):
        email: Optional[EmailStr] = None
        is_active: Optional[bool] = None
        is_verified: Optional[bool] = None
        role: Optional[str] = None

Сервіси для керування користувачами
----------------------------------

Створення користувача
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    def create_user(db: Session, user_in: UserCreate) -> User:
        hashed_password = get_password_hash(user_in.password)
        db_user = User(
            email=user_in.email,
            hashed_password=hashed_password,
            role="user"  # За замовчуванням
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

Оновлення ролі адміністратором
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    def update_user_admin(db: Session, user: User, user_in: UserAdminUpdate) -> User:
        update_data = user_in.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(user, field, value)
        
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

Фільтрація користувачів за роллю
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    def get_users_by_role(db: Session, role: str, skip: int = 0, limit: int = 100) -> List[User]:
        return db.query(User).filter(User.role == role).offset(skip).limit(limit).all()

Підрахунок користувачів за роллю
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    def count_users_by_role(db: Session, role: str) -> int:
        return db.query(User).filter(User.role == role).count()

Тестування ролей
---------------

Unit тести
~~~~~~~~~~

Тести перевіряють:
- Створення користувачів з різними ролями
- Фільтрацію користувачів за роллю
- Перевірку прав доступу
- Відмову в доступі для неавторизованих користувачів

Integration тести
~~~~~~~~~~~~~~~~

Тести перевіряють:
- Доступ до адміністративних ендпоінтів
- Керування користувачами через API
- Обмеження доступу для звичайних користувачів
- Валідацію адміністративних операцій

Приклади використання
--------------------

Створення адміністратора
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    # Створення звичайного користувача
    user_data = UserCreate(
        email="user@example.com",
        password="password"
    )
    user = create_user(db, user_data)
    
    # Підвищення до адміністратора
    update_data = UserAdminUpdate(role="admin")
    admin_user = update_user_admin(db, user, update_data)

Перевірка прав в ендпоінті
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    @router.get("/admin/users")
    def get_all_users(
        current_user: User = Depends(get_current_admin_user),
        db: Session = Depends(get_db)
    ):
        return get_users(db)

Безпека
-------

- Всі адміністративні ендпоінти вимагають автентифікації
- Перевірка ролі виконується на рівні dependency injection
- Адміністратори не можуть видалити себе
- Ролі зберігаються в базі даних з валідацією

Міграції
--------

Для додавання поля role до існуючої бази даних:

.. code-block:: sql

    ALTER TABLE users ADD COLUMN role VARCHAR DEFAULT 'user';
    UPDATE users SET role = 'user' WHERE role IS NULL;
    ALTER TABLE users ALTER COLUMN role SET NOT NULL; 