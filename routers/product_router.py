from fastapi import APIRouter, Depends
from models import product_model
from schemas import product_schema
from repositories import product_repository
from sqlalchemy.orm import Session
from database import engine
from dependencies.get_db import get_db
from utils.user_verification import admin_required
from utils.cache import get_from_cache, set_to_cache

product_model.Base.metadata.create_all(bind=engine)

router = APIRouter(
    prefix="/products",
    tags=["products"],
    dependencies=[Depends(admin_required)]
)

@router.get("/", response_model=list[product_schema.Product])
def read_products(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    cached_products = get_from_cache("cached_products")
    if cached_products:
        print("From cache")
        return cached_products[skip:skip + limit]
    
    products = product_repository.get_products(db=db, skip=skip, limit=limit)
    product_dicts = [product_schema.Product.model_validate(p).model_dump() for p in products]
    set_to_cache("cached_products", product_dicts)
    print("From database")
    return products

@router.get("/{product_id}", response_model=product_schema.Product)
def read_product(product_id: int, db: Session = Depends(get_db)):
    cached_product = get_from_cache(f"product:{product_id}")
    if cached_product:
        print("Cache")
        return cached_product
    product = product_repository.get_product_by_id(db=db, product_id=product_id)
    cached_product = f"product:{product_id}"
    set_to_cache(cached_product, product_schema.Product.model_validate(product).model_dump())
    print("Database")
    return product

@router.post("/", response_model=product_schema.Product)
def create_product(product: product_schema.ProductCreate, db: Session = Depends(get_db)):
    product = product_repository.create_product(db=db, product=product)
    return product

@router.put("/{product_id}", response_model=product_schema.Product)
def update_product(product: product_schema.ProductCreate, product_id: int, db: Session = Depends(get_db)):
    product = product_repository.update_product(db=db, product=product, product_id=product_id)
    return product

@router.delete("/{product_id}", response_model=product_schema.Product)
def delete_product(product_id: int, db: Session = Depends(get_db)):
    product = product_repository.delete_product(db=db, product_id=product_id)
    return product