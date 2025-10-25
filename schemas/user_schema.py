from pydantic import BaseModel, ConfigDict
from datetime import datetime
from enums.user_role import UserRole

class UserBase(BaseModel):
    email: str
    address: str


class UserCreate(UserBase):
    password: str
    role: UserRole


class User(UserBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True