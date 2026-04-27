import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from data.database import Base
from data.repositories import BookRepository, UserRepository, LoanRepository
from data.loans_service import (
    create_loan,
    return_loan,
    UserNotFoundError,
    BookNotFoundError,
    BookAlreadyLoanedError,
    LoanNotFoundError,
)

engine = create_engine("sqlite:///:memory:")
TestSession = sessionmaker(bind=engine)

@pytest.fixture
def db():
    Base.metadata.create_all(bind=engine)
    session = TestSession()
    yield session
    session.close()
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def usuario(db):
    return UserRepository.create(db, name="Test User", email="test@test.com")

@pytest.fixture
def libro(db):
    return BookRepository.create(db, title="Test Book", author="Test Author")

def test_crear_prestamo(db, usuario, libro):
    loan = create_loan(db, user_id=usuario.id, book_id=libro.id)
    assert loan.id is not None
    assert loan.is_active == True

def test_libro_no_disponible_tras_prestamo(db, usuario, libro):
    create_loan(db, user_id=usuario.id, book_id=libro.id)
    assert libro.available == False

def test_no_se_puede_prestar_libro_ya_prestado(db, usuario, libro):
    create_loan(db, user_id=usuario.id, book_id=libro.id)
    with pytest.raises(BookAlreadyLoanedError):
        create_loan(db, user_id=usuario.id, book_id=libro.id)

def test_error_usuario_no_existe(db, libro):
    with pytest.raises(UserNotFoundError):
        create_loan(db, user_id=999, book_id=libro.id)

def test_error_libro_no_existe(db, usuario):
    with pytest.raises(BookNotFoundError):
        create_loan(db, user_id=usuario.id, book_id=999)

def test_devolver_prestamo(db, usuario, libro):
    loan = create_loan(db, user_id=usuario.id, book_id=libro.id)
    loan = return_loan(db, loan_id=loan.id)
    assert loan.is_active == False
    assert libro.available == True

def test_error_devolver_prestamo_no_existe(db):
    with pytest.raises(LoanNotFoundError):
        return_loan(db, loan_id=999)

def test_generador_libros_disponibles(db):
    """Verifica que iter_available genera solo libros disponibles."""
    BookRepository.create(db, title="Libro A", author="Autor A")
    BookRepository.create(db, title="Libro B", author="Autor B")
    b3 = BookRepository.create(db, title="Libro C", author="Autor C")
    b3.available = False
    db.flush()

    disponibles = list(BookRepository.iter_available(db))
    assert len(disponibles) == 2
    assert all(b.available for b in disponibles)

def test_generador_prestamos_activos(db, usuario, libro):
    """Verifica que iter_active genera solo préstamos sin devolver."""
    loan = create_loan(db, user_id=usuario.id, book_id=libro.id)
    db.flush()

    activos = list(LoanRepository.iter_active(db))
    assert len(activos) == 1
    assert activos[0].id == loan.id
