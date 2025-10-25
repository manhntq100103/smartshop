from sqlalchemy.orm import Session
from models import order_model
from schemas import order_schema


def get_order_by_id(db: Session, order_id: int):
    return db.query(order_model.Order).filter(order_model.Order.id == order_id).first()

def get_orders(db: Session, skip: int, limit: int):
    return db.query(order_model.Order).offset(skip).limit(limit).all()

def create_order(db: Session, order: order_schema.OrderCreate):
    db_order = order_model.Order(user_id=order.user_id, product_id=order.product_id, quantity=order.quantity, order_note=order.order_note)
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order

def update_order(db: Session, order: order_schema.OrderCreate, order_id: int):
    db_order = db.query(order_model.Order).filter(order_model.Order.id == order_id).first()
    db_order.user_id = order.user_id
    db_order.product_id = order.product_id
    db_order.quantity = order.quantity
    db_order.order_note = order.order_note
    db.commit()
    db.refresh(db_order)
    return db_order

def delete_order(db: Session, order_id: int):
    db_order = db.query(order_model.Order).filter(order_model.Order.id == order_id).first()
    db.delete(db_order)
    db.commit()
    return db_order