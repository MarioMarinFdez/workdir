from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from data.database import get_session
from data.repositories import UserRepository
from logger import get_logger

logger = get_logger(__name__)

router = APIRouter(prefix="/usuarios", tags=["usuarios"])

def get_db():
    db = get_session()
    try:
        yield db
    finally:
        db.close()

@router.get("/")
def list_users(db: Session = Depends(get_db)):
    logger.info("Listando todos los usuarios")
    users = UserRepository.list_all(db)
    return {"usuarios": [{"id": u.id, "name": u.name, "email": u.email} for u in users]}

@router.post("/")
def create_user(name: str, email: str = None, db: Session = Depends(get_db)):
    logger.info(f"Creando usuario: {name}")
    user = UserRepository.create(db, name=name, email=email)
    db.commit()
    return {"id": user.id, "name": user.name, "email": user.email}
