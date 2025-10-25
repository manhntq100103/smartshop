from sqlalchemy.orm import Session
from models import restock_model
from schemas import restock_schema


def get_restock_by_id(db: Session, restock_id: int):
    return db.query(restock_model.Restock).filter(restock_model.Restock.id == restock_id).first()

def get_restocks(db: Session, skip: int, limit: int):
    return db.query(restock_model.Restock).offset(skip).limit(limit).all()

def create_restock(db: Session, restock: restock_schema.RestockCreate):
    db_restock = restock_model.Restock(product_id=restock.product_id, quantity=restock.quantity)
    db.add(db_restock)
    db.commit()
    db.refresh(db_restock)
    return db_restock

def update_restock(db: Session, restock: restock_schema.RestockCreate, restock_id: int):
    db_restock = db.query(restock_model.Restock).filter(restock_model.Restock.id == restock_id).first()
    db_restock.product_id = restock.product_id
    db_restock.quantity = restock.quantity
    db.commit()
    db.refresh(db_restock)
    return db_restock

def delete_restock(db: Session, restock_id: int):
    db_restock = db.query(restock_model.Restock).filter(restock_model.Restock.id == restock_id).first()
    db.delete(db_restock)
    db.commit()
    return db_restock
