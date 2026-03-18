from data.database import SessionManager
from data.repositories import BookRepository, UserRepository
from data.loans_service import create_loan, return_loan


def main():
    with SessionManager() as session:
        # Crear usuario de prueba
        user = UserRepository.create(
            session,
            name="Usuario Demo",
            email="demo@example.com",
        )
        print("Usuario creado:", user.id, user.name)

        # Crear libro de prueba
        book = BookRepository.create(
            session,
            title="Libro Demo",
            author="Autor Demo",
            isbn="1234567890",
        )
        print("Libro creado:", book.id, book.title)

        # Crear préstamo
        loan = create_loan(session, user_id=user.id, book_id=book.id)
        print("Préstamo creado:", loan.id, "activo:", loan.is_active)

        # Devolver préstamo
        loan = return_loan(session, loan_id=loan.id)
        print("Préstamo devuelto:", loan.id, "activo:", loan.is_active)


if __name__ == "__main__":
    main()
