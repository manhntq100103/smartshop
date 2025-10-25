from sqlalchemy.orm import Session
from models import user_model
from schemas import user_schema

def get_user_by_id(db: Session, user_id: int):
    return db.query(user_model.User).filter(user_model.User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(user_model.User).filter(user_model.User.email == email).first()

def get_users(db: Session, skip: int, limit: int):
    return db.query(user_model.User).offset(skip).limit(limit).all()

def create_user(db: Session, user: user_schema.UserCreate):
    db_user = user_model.User(email=user.email, password=user.password, address=user.address, role=user.role)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, user: user_schema.UserCreate, user_id: int):
    db_user = db.query(user_model.User).filter(user_model.User.id == user_id).first()
    db_user.email = user.email
    db_user.password = user.password
    db_user.address = user.address
    db_user.role = user.role
    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: int):
    db_user = db.query(user_model.User).filter(user_model.User.id == user_id).first()
    db.delete(db_user)
    db.commit()
    return db_user