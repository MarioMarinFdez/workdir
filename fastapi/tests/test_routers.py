import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from data.database import Base
from main import app
from routers.libros import get_db
from routers.usuarios import get_db as get_db_usuarios
from routers.prestamos import get_db as get_db_prestamos

engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
TestSession = sessionmaker(bind=engine)
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

# --- Tests Libros ---

def test_listar_libros_vacio():
    response = client.get("/libros/")
    assert response.status_code == 200

def test_crear_libro():
    response = client.post("/libros/", params={"title": "El Quijote", "author": "Cervantes"})
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "El Quijote"
    assert data["author"] == "Cervantes"

def test_buscar_libro_existente():
    client.post("/libros/", params={"title": "Cien años de soledad", "author": "García Márquez"})
    response = client.get("/libros/buscar/", params={"q": "años"})
    assert response.status_code == 200
    assert len(response.json()["libros"]) >= 1

def test_buscar_libro_no_existente():
    response = client.get("/libros/buscar/", params={"q": "zzznoresult"})
    assert response.status_code == 200
    assert response.json()["libros"] == []

# --- Tests Usuarios ---

def test_listar_usuarios():
    response = client.get("/usuarios/")
    assert response.status_code == 200

def test_crear_usuario():
    response = client.post("/usuarios/", params={"name": "Ana", "email": "ana@test.com"})
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Ana"

# --- Tests Prestamos ---

def test_crear_prestamo_usuario_no_existe():
    response = client.post("/prestamos/", params={"user_id": 9999, "book_id": 1})
    assert response.status_code == 404
    assert response.json()["detail"] == "Usuario no encontrado"

def test_crear_prestamo_libro_no_existe():
    u = client.post("/usuarios/", params={"name": "Carlos", "email": "carlos@test.com"})
    user_id = u.json()["id"]
    response = client.post("/prestamos/", params={"user_id": user_id, "book_id": 9999})
    assert response.status_code == 404
    assert response.json()["detail"] == "Libro no encontrado"

def test_crear_y_devolver_prestamo():
    u = client.post("/usuarios/", params={"name": "Luis", "email": "luis@test.com"})
    b = client.post("/libros/", params={"title": "1984", "author": "Orwell"})
    user_id = u.json()["id"]
    book_id = b.json()["id"]

    r = client.post("/prestamos/", params={"user_id": user_id, "book_id": book_id})
    assert r.status_code == 200
    loan_id = r.json()["id"]

    r2 = client.post(f"/prestamos/{loan_id}/devolver")
    assert r2.status_code == 200

def test_libro_ya_prestado():
    u = client.post("/usuarios/", params={"name": "Sara", "email": "sara@test.com"})
    b = client.post("/libros/", params={"title": "Dune", "author": "Herbert"})
    user_id = u.json()["id"]
    book_id = b.json()["id"]

    client.post("/prestamos/", params={"user_id": user_id, "book_id": book_id})
    r = client.post("/prestamos/", params={"user_id": user_id, "book_id": book_id})
    assert r.status_code == 400
    assert r.json()["detail"] == "Libro ya prestado"
