from sqlalchemy.orm import Session
from models import product_model
from schemas import product_schema

def get_product_by_id(db: Session, product_id: int):
    return db.query(product_model.Product).filter(product_model.Product.id == product_id).first()

def get_products(db: Session, skip: int, limit: int):
    return db.query(product_model.Product).offset(skip).limit(limit).all()

def create_product(db: Session, product: product_schema.ProductCreate):
    db_product = product_model.Product(product_name=product.product_name, category_id=product.category_id, description=product.description, price=product.price)
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def update_product(db: Session, product: product_schema.ProductCreate, product_id: int):
    db_product = db.query(product_model.Product).filter(product_model.Product.id == product_id).first()
    db_product.product_name = product.product_name
    db_product.category_id = product.category_id
    db_product.description = product.description
    db_product.price = product.price
    db.commit()
    db.refresh(db_product)
    return db_product

def delete_product(db: Session, product_id: int):
    db_product = db.query(product_model.Product).filter(product_model.Product.id == product_id).first()
    db.delete(db_product)
    db.commit()
    return db_product