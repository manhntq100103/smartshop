from fastapi import APIRouter, Depends
from models import category_model
from schemas import category_schema
from repositories import category_repository
from sqlalchemy.orm import Session
from database import engine
from dependencies.get_db import get_db

category_model.Base.metadata.create_all(bind=engine)

router = APIRouter(
    prefix="/categories",
    tags=["categories"]
)

@router.get("/", response_model=list[category_schema.Category])
def read_categories(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    categories = category_repository.get_categories(db=db, skip=skip, limit=limit)
    return categories

@router.get("/{category_id}", response_model=category_schema.Category)
def read_category(category_id: int, db: Session = Depends(get_db)):
    category = category_repository.get_category_by_id(db=db, category_id=category_id)
    return category

@router.put("/{category_id}", response_model=category_schema.Category)
def update_category(category: category_schema.CategoryCreate, category_id: int, db: Session = Depends(get_db)):
    category = category_repository.update_category(db=db, category=category, category_id=category_id)
    return category