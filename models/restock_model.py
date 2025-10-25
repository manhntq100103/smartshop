from sqlalchemy import Column, Integer, DateTime, ForeignKey, func
from database import Base

class Restock(Base):
    __tablename__ = "restocks"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    quantity = Column(Integer)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
