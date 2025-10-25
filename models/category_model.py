from database import Base
from sqlalchemy import Column, Integer, String

class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    category_name = Column(String(255), unique=True, index=True)