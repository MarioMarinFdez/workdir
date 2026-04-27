from typing import List, Optional, Generator

from sqlalchemy.orm import Session

from .models import Book, User, Loan


class BookRepository:
    @staticmethod
    def get_by_id(session: Session, book_id: int) -> Optional[Book]:
        return session.get(Book, book_id)

    @staticmethod
    def list_all(session: Session) -> List[Book]:
        return session.query(Book).all()

    @staticmethod
    def iter_available(session: Session) -> Generator[Book, None, None]:
        """Generador que yields libros disponibles uno a uno, sin cargar todos en memoria."""
        query = session.query(Book).filter(Book.available == True).yield_per(50)
        for book in query:
            yield book

    @staticmethod
    def iter_all(session: Session) -> Generator[Book, None, None]:
        """Generador que yields todos los libros uno a uno."""
        query = session.query(Book).yield_per(50)
        for book in query:
            yield book

    @staticmethod
    def create(
        session: Session,
        title: str,
        author: str,
        isbn: str | None = None,
    ) -> Book:
        book = Book(title=title, author=author, isbn=isbn, available=True)
        session.add(book)
        session.flush()
        return book


class UserRepository:
    @staticmethod
    def get_by_id(session: Session, user_id: int) -> Optional[User]:
        return session.get(User, user_id)

    @staticmethod
    def list_all(session: Session) -> List[User]:
        return session.query(User).all()

    @staticmethod
    def create(
        session: Session,
        name: str,
        email: str | None = None,
    ) -> User:
        user = User(name=name, email=email)
        session.add(user)
        session.flush()
        return user


class LoanRepository:
    @staticmethod
    def get_by_id(session: Session, loan_id: int) -> Optional[Loan]:
        return session.get(Loan, loan_id)

    @staticmethod
    def get_active_loan_for_book(session: Session, book_id: int) -> Optional[Loan]:
        return (
            session.query(Loan)
            .filter(Loan.book_id == book_id, Loan.return_date.is_(None))
            .one_or_none()
        )

    @staticmethod
    def list_active(session: Session) -> List[Loan]:
        return session.query(Loan).filter(Loan.return_date.is_(None)).all()

    @staticmethod
    def iter_active(session: Session) -> Generator[Loan, None, None]:
        """Generador que yields préstamos activos uno a uno."""
        query = session.query(Loan).filter(Loan.return_date.is_(None)).yield_per(50)
        for loan in query:
            yield loan
    
    @staticmethod
    def get_loans_by_user(session: Session, user_id: int) -> List[Loan]:
        return (
            session.query(Loan)
            .filter(Loan.user_id == user_id)
            .order_by(Loan.loan_date.desc())
            .all()
        )
    @staticmethod
    def create(
        session: Session,
        user: User,
        book: Book,
        loan_date,
        due_date,
    ) -> Loan:
        loan = Loan(
            user_id=user.id,
            book_id=book.id,
            loan_date=loan_date,
            due_date=due_date,
        )
        session.add(loan)
        session.flush()
        return loan
