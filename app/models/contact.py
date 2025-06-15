from sqlalchemy import Column, ForeignKey, Integer, String, Date, Text
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class Contact(Base):
    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    phone = Column(String)
    birthday = Column(Date, nullable=True)
    additional_data = Column(String, nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="contacts") 