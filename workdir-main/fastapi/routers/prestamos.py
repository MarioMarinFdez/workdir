from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from dependencies import get_db
from data.models import Loan
from data.repositories import UserRepository
from data.loans_service import (
    create_loan, return_loan,
    UserNotFoundError, BookNotFoundError,
    BookAlreadyLoanedError, LoanNotFoundError,
)
from logger import get_logger

logger = get_logger(__name__)

router = APIRouter(prefix="/prestamos", tags=["prestamos"])

@router.post("/")
def create_loan_endpoint(user_id: int, book_id: int, db: Session = Depends(get_db)):
    logger.info(f"Creando prestamo: usuario {user_id}, libro {book_id}")
    try:
        loan = create_loan(db, user_id=user_id, book_id=book_id)
        db.commit()
        return {"id": loan.id, "user_id": loan.user_id, "book_id": loan.book_id, "loan_date": loan.loan_date}
    except UserNotFoundError:
        logger.warning(f"Usuario no encontrado: {user_id}")
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    except BookNotFoundError:
        logger.warning(f"Libro no encontrado: {book_id}")
        raise HTTPException(status_code=404, detail="Libro no encontrado")
    except BookAlreadyLoanedError:
        logger.warning(f"Libro ya prestado: {book_id}")
        raise HTTPException(status_code=400, detail="Libro ya prestado")

@router.post("/{loan_id}/devolver")
def return_loan_endpoint(loan_id: int, db: Session = Depends(get_db)):
    logger.info(f"Devolviendo prestamo: {loan_id}")
    try:
        loan = return_loan(db, loan_id=loan_id)
        db.commit()
        return {"id": loan.id, "return_date": loan.return_date}
    except LoanNotFoundError:
        logger.error(f"Prestamo no encontrado: {loan_id}")
        raise HTTPException(status_code=404, detail="Préstamo no encontrado")

@router.get("/usuario/{user_id}")
def get_user_loans(user_id: int, db: Session = Depends(get_db)):
    logger.info(f"Consultando historial del usuario {user_id}")
    user = UserRepository.get_by_id(db, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    loans = db.query(Loan).filter(Loan.user_id == user_id).all()
    return {
        "usuario": user.name,
        "prestamos": [
            {
                "loan_id": l.id,
                "book_title": l.book.title,
                "loan_date": l.loan_date,
                "due_date": l.due_date,
                "return_date": l.return_date,
                "activo": l.is_active,
                "vencido": l.is_overdue,
            }
            for l in loans
        ]
    }
