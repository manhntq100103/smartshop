from pydantic import BaseModel, ConfigDict

class ProductBase(BaseModel):
    product_name: str
    price: float
    description: str


class ProductCreate(ProductBase):
    category_id: int


class Product(ProductBase):
    id: int

    class Config:
        from_attributes = True