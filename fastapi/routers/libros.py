from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from data.database import get_session
from data.repositories import BookRepository
from logger import get_logger
from decorators import log_execution_time

logger = get_logger(__name__)

router = APIRouter(prefix="/libros", tags=["libros"])

def get_db():
    db = get_session()
    try:
        yield db
    finally:
        db.close()

@router.get("/")
@log_execution_time
def list_books(db: Session = Depends(get_db)):
    logger.info("Listando todos los libros")
    books = BookRepository.list_all(db)
    return {"libros": [{"id": b.id, "title": b.title, "author": b.author, "available": b.available} for b in books]}

@router.post("/")
@log_execution_time
def create_book(title: str, author: str, isbn: str = None, db: Session = Depends(get_db)):
    logger.info(f"Creando libro: {title} de {author}")
    book = BookRepository.create(db, title=title, author=author, isbn=isbn)
    db.commit()
    return {"id": book.id, "title": book.title, "author": book.author}

@router.get("/buscar/")
@log_execution_time
def search_books(q: str, db: Session = Depends(get_db)):
    logger.info(f"Buscando libros con: {q}")
    books = BookRepository.list_all(db)
    q_lower = q.lower()
    results = [b for b in books if q_lower in b.title.lower() or q_lower in b.author.lower()]
    if not results:
        logger.warning(f"No se encontraron libros para: {q}")
    return {"libros": [{"id": b.id, "title": b.title, "author": b.author, "available": b.available} for b in results]}
