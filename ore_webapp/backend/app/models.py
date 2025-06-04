
from sqlalchemy import Column, Integer, String, Boolean, LargeBinary, Float, ForeignKey

from sqlalchemy import Column, Integer, String, Boolean, LargeBinary, ForeignKey, Date, DateTime

from sqlalchemy.orm import relationship
from datetime import datetime

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



class Report(Base):
    __tablename__ = "reports"

    id = Column(Integer, primary_key=True, index=True)
    reference = Column(String, unique=True, index=True)
    details = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    tags = Column(String)
    priority = Column(String)
    follow_up = Column(Boolean, default=False)
    status = Column(String, default="open")
    files = relationship("ReportFile", back_populates="report")


class ReportFile(Base):
    __tablename__ = "report_files"

    id = Column(Integer, primary_key=True, index=True)
    report_id = Column(Integer, ForeignKey("reports.id"))
    file_id = Column(Integer, ForeignKey("files.id"))
    report = relationship("Report", back_populates="files")
    file = relationship("StoredFile")

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, default="")
    phase = Column(String, index=True)
    urgency = Column(String, index=True)
    location = Column(String, index=True)
    status = Column(String, default="todo", index=True)
    responsible_id = Column(Integer, ForeignKey("users.id"))
    due_date = Column(Date, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    responsible = relationship("User")

