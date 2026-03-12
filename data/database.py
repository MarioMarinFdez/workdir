from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Por ahora, BD SQLite local en un fichero
DATABASE_URL = "sqlite:///./library.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},  # necesario para SQLite en algunos entornos
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_session():
    return SessionLocal()


class SessionManager:
    def __enter__(self):
        self.session = SessionLocal()
        return self.session

    def __exit__(self, exc_type, exc, tb):
        if exc_type is not None:
            self.session.rollback()
        else:
            self.session.commit()
        self.session.close()

