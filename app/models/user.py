from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class User(Base):
    """
    User model for storing user information.
    
    Attributes:
        id (int): Primary key
        email (str): User's email address (unique)
        hashed_password (str): Hashed password
        is_active (bool): Whether the user is active
        is_verified (bool): Whether the user's email is verified
        role (str): User's role ('user' or 'admin')
        contacts (List[Contact]): User's contacts
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    role = Column(String, default="user")  # 'user' or 'admin'
    contacts = relationship("Contact", back_populates="owner") 