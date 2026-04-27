import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    DateTime,
    ForeignKey,
)
from sqlalchemy.orm import relationship

from .database import Base


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)
    genre = Column(String, nullable=True)
    isbn = Column(String, nullable=True, unique=True)
    available = Column(Boolean, default=True)

    loans = relationship("Loan", back_populates="book")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=True, unique=True)

    loans = relationship("Loan", back_populates="user")

    @property
    def display_name(self) -> str:
        return self.name


class Loan(Base):
    __tablename__ = "loans"

    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, ForeignKey("books.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    loan_date = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)
    due_date = Column(DateTime, nullable=True)
    return_date = Column(DateTime, nullable=True)

    book = relationship("Book", back_populates="loans")
    user = relationship("User", back_populates="loans")

    @property
    def is_active(self) -> bool:
        return self.return_date is None

    @property
    def is_overdue(self) -> bool:
        return (
            self.return_date is None
            and self.due_date is not None
            and self.due_date < datetime.datetime.utcnow()
        )
