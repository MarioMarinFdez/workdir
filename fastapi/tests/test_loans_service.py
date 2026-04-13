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

# Base de datos en memoria para tests
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
