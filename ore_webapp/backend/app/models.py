from sqlalchemy import Column, Integer, String, Boolean, LargeBinary
from sqlalchemy.orm import relationship

from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    files = relationship("StoredFile", back_populates="owner")

class StoredFile(Base):
    __tablename__ = "files"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, index=True)
    data = Column(LargeBinary)
    owner_id = Column(Integer)
    owner = relationship("User", back_populates="files")
