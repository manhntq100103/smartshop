from sqlalchemy.orm import Session
from models import category_model
from schemas import category_schema


def get_category_by_id(db: Session, category_id: int):
    return db.query(category_model.Category).filter(category_model.Category.id == category_id).first()

def get_categories(db: Session, skip: int, limit: int):
    return db.query(category_model.Category).offset(skip).limit(limit).all()

def update_category(db: Session, category: category_schema.CategoryCreate, category_id: int):
    db_category = db.query(category_model.Category).filter(category_model.Category.id == category_id).first()
    db_category.category_name = category.category_name
    db.commit()
    db.refresh(db_category)
    return db_category
