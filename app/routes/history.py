from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional
from app.auth_utils import get_current_user
from app.models.user import User
from app.models.history import History
from app.database import get_db

router = APIRouter(prefix="/api/history", tags=["history"])

class HistoryCreate(BaseModel):
    tool_name: str
    session_data: Optional[str] = None

class HistoryResponse(BaseModel):
    id: int
    tool_name: str
    session_data: Optional[str]
    created_at: str

    class Config:
        from_attributes = True

@router.get("/", response_model=List[HistoryResponse])
def get_history(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    history_items = db.query(History).filter(History.user_id == current_user.id).order_by(History.created_at.desc()).all()
    return [
        {
            "id": item.id,
            "tool_name": item.tool_name,
            "session_data": item.session_data,
            "created_at": item.created_at.isoformat() if item.created_at else ""
        }
        for item in history_items
    ]

@router.post("/", response_model=HistoryResponse)
def create_history(payload: HistoryCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    history_item = History(
        user_id=current_user.id,
        tool_name=payload.tool_name,
        session_data=payload.session_data
    )
    db.add(history_item)
    db.commit()
    db.refresh(history_item)

    return {
        "id": history_item.id,
        "tool_name": history_item.tool_name,
        "session_data": history_item.session_data,
        "created_at": history_item.created_at.isoformat() if history_item.created_at else ""
    }

@router.delete("/{history_id}")
def delete_history(history_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    history_item = db.query(History).filter(History.id == history_id, History.user_id == current_user.id).first()
    if not history_item:
        raise HTTPException(status_code=404, detail="History item not found")

    db.delete(history_item)
    db.commit()
    return {"message": "History item deleted"}
