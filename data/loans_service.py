import datetime

from sqlalchemy.orm import Session

from data.repositories import BookRepository, UserRepository, LoanRepository


class UserNotFoundError(Exception):
    pass


class BookNotFoundError(Exception):
    pass


class BookAlreadyLoanedError(Exception):
    pass


class LoanNotFoundError(Exception):
    pass


def create_loan(
    session: Session,
    user_id: int,
    book_id: int,
    days: int = 15,
):
    user = UserRepository.get_by_id(session, user_id)
    if user is None:
        raise UserNotFoundError(f"User {user_id} not found")

    book = BookRepository.get_by_id(session, book_id)
    if book is None:
        raise BookNotFoundError(f"Book {book_id} not found")

    active_loan = LoanRepository.get_active_loan_for_book(session, book_id)
    if active_loan is not None:
        raise BookAlreadyLoanedError(f"Book {book_id} already loaned")

    loan_date = datetime.datetime.utcnow()
    due_date = loan_date + datetime.timedelta(days=days)

    loan = LoanRepository.create(
        session=session,
        user=user,
        book=book,
        loan_date=loan_date,
        due_date=due_date,
    )

    book.available = False

    return loan


def return_loan(session: Session, loan_id: int):
    loan = LoanRepository.get_by_id(session, loan_id)
    if loan is None:
        raise LoanNotFoundError(f"Loan {loan_id} not found")

    if loan.return_date is not None:
        return loan

    loan.return_date = datetime.datetime.utcnow()
    loan.book.available = True

    return loan
