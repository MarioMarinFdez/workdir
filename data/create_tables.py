from data.database import Base, engine
import data.models  # noqa: F401  # Importa modelos para registrarlos en Base


def main():
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    main()
