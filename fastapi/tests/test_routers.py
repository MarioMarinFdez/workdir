import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import data.models
from data.database import Base
import data.database as db_module
from main import app
from routers.libros import get_db
from routers.usuarios import get_db as get_db_usuarios
from routers.prestamos import get_db as get_db_prestamos

TEST_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestSession = sessionmaker(bind=engine)
db_module.engine = engine
db_module.SessionLocal = TestSession
Base.metadata.create_all(bind=engine)

def override_get_db():
    db = TestSession()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_db_usuarios] = override_get_db
app.dependency_overrides[get_db_prestamos] = override_get_db
client = TestClient(app)
