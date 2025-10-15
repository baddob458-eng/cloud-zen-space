from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from typing import Optional
from passlib.context import CryptContext
from app.auth_utils import get_current_user
from app.models.user import User
from app.database import get_db

router = APIRouter(prefix="/api/profile", tags=["profile"])
pwd = CryptContext(schemes=["bcrypt"], deprecated="auto")

class ProfileResponse(BaseModel):
    id: int
    username: str
    email: str

    class Config:
        from_attributes = True

class ProfileUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    current_password: Optional[str] = None
    new_password: Optional[str] = None

@router.get("/", response_model=ProfileResponse)
def get_profile(current_user: User = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "username": current_user.username,
        "email": current_user.email
    }

@router.put("/", response_model=ProfileResponse)
def update_profile(payload: ProfileUpdate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if payload.username:
        current_user.username = payload.username

    if payload.email:
        existing = db.query(User).filter(User.email == payload.email, User.id != current_user.id).first()
        if existing:
            raise HTTPException(status_code=400, detail="Email already in use")
        current_user.email = payload.email

    if payload.new_password:
        if not payload.current_password:
            raise HTTPException(status_code=400, detail="Current password required to change password")
        if not pwd.verify(payload.current_password, current_user.hashed_password):
            raise HTTPException(status_code=400, detail="Current password is incorrect")
        current_user.hashed_password = pwd.hash(payload.new_password)

    db.commit()
    db.refresh(current_user)

    return {
        "id": current_user.id,
        "username": current_user.username,
        "email": current_user.email
    }

@router.delete("/")
def delete_profile(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    db.delete(current_user)
    db.commit()
    return {"message": "Profile deleted successfully"}
