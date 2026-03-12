from fastapi import Depends
from sqlalchemy.orm import Session
from fastapi import HTTPException
from data.database import get_session
from data.repositories import BookRepository, UserRepository
from data.loans_service import (
    create_loan,
    return_loan,
    UserNotFoundError,
    BookNotFoundError,
    BookAlreadyLoanedError,
    LoanNotFoundError,
)
def get_db_session():
    db = get_session()
    try:
        yield db
    finally:
        db.close()
@app.post("/users")
def create_user(
    name: str,
    email: str | None = None,
    db: Session = Depends(get_db_session),
):
    user = UserRepository.create(db, name=name, email=email)
    return {"id": user.id, "name": user.name, "email": user.email}


@app.post("/books")
def create_book(
    title: str,
    author: str,
    isbn: str | None = None,
    db: Session = Depends(get_db_session),
):
    book = BookRepository.create(db, title=title, author=author, isbn=isbn)
    return {"id": book.id, "title": book.title, "author": book.author, "isbn": book.isbn}


@app.post("/loans")
def create_loan_endpoint(
    user_id: int,
    book_id: int,
    db: Session = Depends(get_db_session),
):
    try:
        loan = create_loan(db, user_id=user_id, book_id=book_id)
        return {
            "id": loan.id,
            "user_id": loan.user_id,
            "book_id": loan.book_id,
            "loan_date": loan.loan_date,
            "due_date": loan.due_date,
            "return_date": loan.return_date,
        }
    except UserNotFoundError:
        raise HTTPException(status_code=404, detail="User not found")
    except BookNotFoundError:
        raise HTTPException(status_code=404, detail="Book not found")
    except BookAlreadyLoanedError:
        raise HTTPException(status_code=400, detail="Book already loaned")


@app.post("/loans/{loan_id}/return")
def return_loan_endpoint(
    loan_id: int,
    db: Session = Depends(get_db_session),
):
    try:
        loan = return_loan(db, loan_id=loan_id)
        return {
            "id": loan.id,
            "user_id": loan.user_id,
            "book_id": loan.book_id,
            "loan_date": loan.loan_date,
            "due_date": loan.due_date,
            "return_date": loan.return_date,
        }
    except LoanNotFoundError:
        raise HTTPException(status_code=404, detail="Loan not found")
