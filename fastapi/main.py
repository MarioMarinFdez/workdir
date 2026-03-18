from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from data.database import get_session, Base, engine
from data.repositories import BookRepository, UserRepository, LoanRepository
from data.loans_service import (
    create_loan,
    return_loan,
    UserNotFoundError,
    BookNotFoundError,
    BookAlreadyLoanedError,
    LoanNotFoundError,
)

# Crear tablas al arrancar
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Gestor de Bibliotecas API",
    description="Servidor de datos para la gestión de bibliotecas.",
    version="2.0.0",
)

def get_db():
    db = get_session()
    try:
        yield db
    finally:
        db.close()

@app.get("/libros/")
def list_books(db: Session = Depends(get_db)):
    books = BookRepository.list_all(db)
    return {"libros": [{"id": b.id, "title": b.title, "author": b.author, "available": b.available} for b in books]}

@app.post("/libros/")
def create_book(title: str, author: str, isbn: str = None, db: Session = Depends(get_db)):
    book = BookRepository.create(db, title=title, author=author, isbn=isbn)
    db.commit()
    return {"id": book.id, "title": book.title, "author": book.author}

@app.get("/usuarios/")
def list_users(db: Session = Depends(get_db)):
    users = UserRepository.list_all(db)
    return {"usuarios": [{"id": u.id, "name": u.name, "email": u.email} for u in users]}

@app.post("/usuarios/")
def create_user(name: str, email: str = None, db: Session = Depends(get_db)):
    user = UserRepository.create(db, name=name, email=email)
    db.commit()
    return {"id": user.id, "name": user.name, "email": user.email}

@app.post("/prestamos/")
def create_loan_endpoint(user_id: int, book_id: int, db: Session = Depends(get_db)):
    try:
        loan = create_loan(db, user_id=user_id, book_id=book_id)
        db.commit()
        return {"id": loan.id, "user_id": loan.user_id, "book_id": loan.book_id, "loan_date": loan.loan_date}
    except UserNotFoundError:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    except BookNotFoundError:
        raise HTTPException(status_code=404, detail="Libro no encontrado")
    except BookAlreadyLoanedError:
        raise HTTPException(status_code=400, detail="Libro ya prestado")

@app.post("/prestamos/{loan_id}/devolver")
def return_loan_endpoint(loan_id: int, db: Session = Depends(get_db)):
    try:
        loan = return_loan(db, loan_id=loan_id)
        db.commit()
        return {"id": loan.id, "return_date": loan.return_date}
    except LoanNotFoundError:
        raise HTTPException(status_code=404, detail="Préstamo no encontrado")
