from database import Base
from sqlalchemy import Column, Integer, String, Enum, DateTime, func
from enums.user_role import UserRole

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255))
    password = Column(String(255))
    address = Column(String(255))
    role = Column(Enum(UserRole), default=UserRole.customer)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
