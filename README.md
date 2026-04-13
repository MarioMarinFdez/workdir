# Práctica Final: Gestor de Bibliotecas 📚

Sistema completo de **Gestión de Bibliotecas** con backend en FastAPI, base de datos SQLAlchemy, interfaz gráfica en Streamlit y despliegue con Docker Compose.

---

## 🚀 Arrancar el proyecto

```bash
docker compose up --build
```

- **API (FastAPI):** http://localhost:8000/docs
- **Interfaz (Streamlit):** http://localhost:8501

---

## Tecnologías

- **Python 3.10+**
- **FastAPI** — API REST con APIRouter
- **SQLAlchemy 2.x** — ORM con SQLite
- **Streamlit** — Interfaz gráfica
- **Pytest + pytest-cov** — Tests con cobertura ≥ 80%
- **Docker + Docker Compose** — Despliegue en contenedores
- **GitHub Actions** — CI/CD automático en cada push

---

## 🧱 Principios SOLID aplicados

### SRP — Single Responsibility Principle
- `BookRepository`, `UserRepository`, `LoanRepository` → solo acceso a datos de su entidad.
- `loans_service.py` → solo lógica de negocio de préstamos.
- `logger.py` → solo configuración del sistema de logs.
- Los routers (`libros.py`, `usuarios.py`, `prestamos.py`) gestionan únicamente su dominio.

### OCP — Open/Closed Principle
Los repositorios están diseñados para ser extendidos sin modificar. Si se necesita un `PostgreSQLBookRepository`, basta con crear una nueva clase sin tocar el código existente. El decorador `@log_execution_time` se aplica a cualquier función sin modificarla.

### LSP — Liskov Substitution Principle
Los modelos `Book`, `User` y `Loan` heredan de `Base` y pueden sustituirse por subclases sin romper el sistema. Los `@property` (`is_active`, `is_overdue`, `display_name`) se comportan de forma consistente en cualquier contexto.

### ISP — Interface Segregation Principle
Los repositorios están segregados por entidad. Los routers de FastAPI están separados por dominio, de forma que cada cliente solo usa los endpoints que necesita.

### DIP — Dependency Inversion Principle
Los routers dependen de la abstracción `get_db()` inyectada vía `Depends`. El servicio `loans_service.py` recibe la sesión como parámetro, facilitando los tests con BD en memoria.

---

## 🔁 Metodología XP

- **Pair Programming**: commits con `Co-authored-by`.
- **TDD**: tests escritos antes que la implementación.
- **Integración Continua**: GitHub Actions en cada push. Ver `.github/workflows/ci.yml`.
- **Stand-ups Diarios**: registrados en `DAILYS.md`.

---

## 🧪 Ejecutar tests localmente

```bash
cd fastapi
pip install -r requirements.txt
pip install pytest pytest-cov
pytest tests/ -v --cov=. --cov-report=term-missing
```

---

## ✨ Técnicas avanzadas implementadas

| Técnica | Dónde |
|---|---|
| **Decoradores propios** | `fastapi/decorators.py` → `@log_execution_time` |
| **@property** | `data/models.py` → `is_active`, `is_overdue`, `display_name` |
| **Context Manager** | `data/database.py` → `SessionManager` con `with` |
| **Generadores** | `data/repositories.py` → `iter_all()` con `yield` |
| **Excepciones personalizadas** | `data/loans_service.py` → `UserNotFoundError`, etc. |
| **Logging multinivel** | `fastapi/logger.py` → INFO, WARNING, ERROR |
| **Caché en Streamlit** | `streamlit/pages/1_List_Books.py` → `@st.cache_data` |
