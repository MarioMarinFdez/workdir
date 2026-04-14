from fastapi import FastAPI
from data.database import Base, engine
from routers import libros, usuarios, prestamos

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Gestor de Bibliotecas API",
    description="Servidor de datos para la gestión de bibliotecas.",
    version="2.0.0",
)

app.include_router(libros.router)
app.include_router(usuarios.router)
app.include_router(prestamos.router)
