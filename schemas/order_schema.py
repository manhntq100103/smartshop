from pydantic import BaseModel, ConfigDict
from datetime import datetime

class OrderBase(BaseModel):
    user_id: int
    product_id: int
    quantity: int
    order_note: str


class OrderCreate(OrderBase):
    pass

class Order(OrderBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True