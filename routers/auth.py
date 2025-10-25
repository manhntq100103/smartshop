from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from pydantic import BaseModel
from repositories import user_repository
from sqlalchemy.orm import Session
from dependencies.get_db import get_db

# from utils.verify_password import verify_password
from utils.create_access_token import create_access_token

router = APIRouter()

class LoginRequest(BaseModel):
    email: str
    password: str

@router.post("/login")
def get_auth(request: LoginRequest, db: Session = Depends(get_db)):
    user = user_repository.get_user_by_email(db=db, email=request.email)
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # if not verify_password(password, user.password):
    #     raise HTTPException(status_code=401, detail="Incorrect password")
    
    if request.password != user.password:
        raise HTTPException(status_code=401, detail="Incorrect password")
    
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}