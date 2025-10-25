from fastapi import APIRouter, Depends
from models import restock_model
from schemas import restock_schema
from repositories import restock_repository
from sqlalchemy.orm import Session
from database import engine
from dependencies.get_db import get_db
from utils.user_verification import admin_required
from utils.cache import get_from_cache, set_to_cache

restock_model.Base.metadata.create_all(bind=engine)

router = APIRouter(
    prefix="/restocks",
    tags=["restocks"],
    dependencies=[Depends(admin_required)]
)

@router.get("/", response_model=list[restock_schema.Restock])
def read_restocks(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    cached_restocks = get_from_cache("cached_restocks")
    if cached_restocks:
        return cached_restocks
    
    restocks = restock_repository.get_restocks(db=db, skip=skip, limit=limit)
    restock_dicts = [restock_schema.Restock.model_validate(r).model_dump() for r in restocks]
    return restock_dicts

@router.get("/{restock_id}", response_model=restock_schema.Restock)
def read_restock(restock_id: int, db: Session = Depends(get_db)):
    cached_restock = get_from_cache(f"restock:{restock_id}")
    if cached_restock:
        return cached_restock
    restock = restock_repository.get_restock_by_id(db=db, restock_id=restock_id)
    cached_restock = f"restock:{restock_id}"
    set_to_cache(cached_restock, restock_schema.Restock.model_validate(restock).model_dump())
    return restock

@router.post("/", response_model=restock_schema.Restock)
def read_restock(restock: restock_schema.RestockCreate, db: Session = Depends(get_db)):
    restock = restock_repository.get_restock_by_id(db=db, restock=restock)
    return restock

@router.put("/{restock_id}", response_model=restock_schema.Restock)
def read_restock(restock_id: int, restock: restock_schema.RestockCreate, db: Session = Depends(get_db)):
    restock = restock_repository.get_restock_by_id(db=db, restock=restock, restock_id=restock_id)
    return restock

@router.get("/{restock_id}", response_model=restock_schema.Restock)
def read_restock(restock_id: int, db: Session = Depends(get_db)):
    restock = restock_repository.delete_restock(db=db, restock_id=restock_id)
    return restock