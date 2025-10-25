from fastapi import APIRouter, Depends
from models import order_model
from schemas import order_schema
from repositories import order_repository
from sqlalchemy.orm import Session
from database import engine
from dependencies.get_db import get_db
from utils.user_verification import admin_required
from utils.cache import get_from_cache, set_to_cache

order_model.Base.metadata.create_all(bind=engine)

router = APIRouter(
    prefix="/orders",
    tags=["orders"],
    dependencies=[Depends(admin_required)]
)

@router.get("/", response_model=list[order_schema.Order])
def read_orders(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    cached_orders = get_from_cache("cached_orders")
    if cached_orders:
        return cached_orders[skip:skip + limit]
    
    orders = order_repository.get_orders(db=db, skip=skip, limit=limit)
    order_dicts = [order_schema.Order.model_validate(o).model_dump() for o in order_dicts]
    set_to_cache("cached_orders", order_dicts)
    return orders

@router.get("/{order_id}", response_model=order_schema.Order)
def read_order(order_id: int, db: Session = Depends(get_db)):
    cached_order = get_from_cache(f"order:{order_id}")
    if cached_order:
        return cached_order
    order = order_repository.get_order_by_id(db=db, order_id=order_id)
    cached_order = f"order:{order_id}"
    set_to_cache(cached_order, order_schema.Order.model_validate(order).model_dump())
    return order

@router.post("/", response_model=order_schema.Order)
def create_order(order: order_schema.OrderCreate, db: Session = Depends(get_db)):
    order = order_repository.create_order(db=db, order=order)
    return order

@router.put("/", response_model=order_schema.Order)
def update_order(order: order_schema.Order, order_id: int, db: Session = Depends(get_db)):
    order = order_repository.update_order(db=db, order=order, order_id=order_id)
    return order

@router.put("/", response_model=order_schema.Order)
def delete_order(order_id: int, db: Session = Depends(get_db)):
    order = order_repository.delete_order(db=db, order_id=order_id)
    return order