from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from pydantic import BaseModel, EmailStr
from datetime import datetime, timedelta
from jose import jwt
from app.database import get_db
from app.models.user import User
from app.config import settings

router = APIRouter(prefix="/api/auth", tags=["auth"])
pwd = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.JWT_ALGORITHM)

@router.post("/signup")
def signup(payload: UserCreate, db: Session = Depends(get_db)):
    # prevent duplicate
    if db.query(User).filter(User.email == payload.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed = pwd.hash(payload.password)
    user = User(username=payload.username, email=payload.email, hashed_password=hashed)
    db.add(user)
    db.commit()
    db.refresh(user)

    token = create_access_token({"sub": user.email})
    return {"user": {"id": user.id, "username": user.username, "email": user.email}, "access_token": token, "token_type": "bearer"}

@router.post("/login")
def login(payload: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == payload.email).first()
    if not db_user or not pwd.verify(payload.password, db_user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    token = create_access_token({"sub": db_user.email})
    return {"user": {"id": db_user.id, "username": db_user.username, "email": db_user.email}, "access_token": token, "token_type": "bearer"}

@router.post("/logout")
def logout():
    return {"message": "Logged out successfully"}

@router.post("/google")
def google_oauth(db: Session = Depends(get_db)):
    return {
        "message": "Google OAuth not yet configured",
        "instructions": "Add GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET to .env file"
    }

@router.post("/apple")
def apple_oauth(db: Session = Depends(get_db)):
    return {
        "message": "Apple OAuth not yet configured",
        "instructions": "Add APPLE_CLIENT_ID and APPLE_CLIENT_SECRET to .env file"
    }

@router.get("/ping")
def ping():
    return {"msg": "auth alive"}
