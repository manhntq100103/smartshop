from pydantic import BaseModel, ConfigDict
from datetime import datetime

class RestockBase(BaseModel):
    product_id: int


class RestockCreate(RestockBase):
    quantity: int


class Restock(RestockBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True