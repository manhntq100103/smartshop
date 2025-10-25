from database import Base
from sqlalchemy import Column, Integer, String, Float, ForeignKey

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    product_name = Column(String(255))
    category_id = Column(Integer, ForeignKey("categories.id"))
    description = Column(String(255), default="No description")
    price = Column(Float)