from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from dependencies import get_db
from data.repositories import UserRepository
from logger import get_logger

logger = get_logger(__name__)

router = APIRouter(prefix="/usuarios", tags=["usuarios"])

@router.get("/")
def list_users(db: Session = Depends(get_db)):
    logger.info("Listando todos los usuarios")
    users = UserRepository.list_all(db)
    return {"usuarios": [{"id": u.id, "name": u.name, "email": u.email} for u in users]}

@router.post("/")
def create_user(name: str, email: str = None, db: Session = Depends(get_db)):
    logger.info(f"Creando usuario: {name}")
    try:
        user = UserRepository.create(db, name=name, email=email)
        db.commit()
        return {"id": user.id, "name": user.name, "email": user.email}
    except IntegrityError:
        db.rollback()
        logger.warning(f"Email duplicado: {email}")
        raise HTTPException(status_code=400, detail="El email ya está registrado")