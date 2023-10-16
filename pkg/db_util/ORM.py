from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

# Create a declarative base
DeclarativeBase = declarative_base()


class Base(DeclarativeBase):
    """
    Base class provides a set of common functionality for declarative models.
    It is used as a base class for our User and Upload classes to inherit from.
    This allows SQLAlchemy to track and manage the defined models.
    """
    __abstract__ = True


class User(Base):
    """
    Class User represents a user in the system with a unique email address.
    It has a one-to-many relationship with the Upload class, representing the files uploaded by the user.
    """

    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, nullable=False)
    uploads = relationship("Upload", back_populates="user", cascade="all, delete")


class Upload(Base):
    """
    Class Upload represents an uploaded file in the system.
    It has a foreign key reference to the User model and a one-to-many relationship with the User class.
    """

    __tablename__ = "uploads"
    id = Column(Integer, primary_key=True)
    uid = Column(String, nullable=False)
    filename = Column(String, nullable=False)
    upload_time = Column(DateTime, nullable=False)
    finish_time = Column(DateTime)
    status = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="uploads")
