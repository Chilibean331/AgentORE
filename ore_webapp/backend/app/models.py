from sqlalchemy import Column, Integer, String, Boolean, LargeBinary, Float, ForeignKey
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
