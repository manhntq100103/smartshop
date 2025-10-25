from fastapi import APIRouter, Depends
from models import user_model
from schemas import user_schema
from repositories import user_repository
from sqlalchemy.orm import Session
from database import engine
from dependencies.get_db import get_db

user_model.Base.metadata.create_all(bind=engine)

router = APIRouter(
    prefix="/users",
    tags=["users"]
)

@router.get("/", response_model=list[user_schema.User])
def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    users = user_repository.get_users(db=db, skip=skip, limit=limit)
    return users

@router.get("/{user_id}", response_model=user_schema.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    user = user_repository.get_user_by_id(db=db, user_id=user_id)
    return user

@router.post("/", response_model=user_schema.User)
def create_user(user: user_schema.UserCreate, db: Session = Depends(get_db)):
    user = user_repository.create_user(db=db, user=user)
    return user

@router.put("/{user_id}", response_model=user_schema.User)
def update_user(user: user_schema.UserCreate, user_id: int, db: Session = Depends(get_db)):
    user = user_repository.update_user(db=db, user=user, user_id=user_id)
    return user

@router.delete("/{user_id}", response_model=user_schema.User)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = user_repository.delete_user(db=db, user_id=user_id)
    return user