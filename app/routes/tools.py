from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List
from app.auth_utils import get_current_user
from app.models.user import User
from app.models.tool import ConnectedTool
from app.database import get_db

router = APIRouter(prefix="/api/tools", tags=["tools"])

AVAILABLE_TOOLS = [
    {"id": "chatgpt", "name": "ChatGPT", "category": "AI Assistant", "description": "AI-powered chatbot"},
    {"id": "capcut", "name": "CapCut", "category": "Video Editing", "description": "Video editor"},
    {"id": "zoom", "name": "Zoom", "category": "Communication", "description": "Video conferencing"},
    {"id": "canva", "name": "Canva", "category": "Design", "description": "Graphic design tool"},
    {"id": "notion", "name": "Notion", "category": "Productivity", "description": "Workspace and notes"},
    {"id": "figma", "name": "Figma", "category": "Design", "description": "UI/UX design tool"}
]

class ToolConnect(BaseModel):
    tool_id: str

class ToolResponse(BaseModel):
    id: int
    tool_id: str
    tool_name: str
    status: str
    category: str

@router.get("/list")
def list_available_tools():
    return {"tools": AVAILABLE_TOOLS}

@router.get("/connected")
def get_connected_tools(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    connected = db.query(ConnectedTool).filter(ConnectedTool.user_id == current_user.id).all()
    return {
        "tools": [
            {
                "id": tool.id,
                "tool_id": tool.tool_id,
                "tool_name": tool.tool_name,
                "status": tool.status,
                "category": tool.category
            }
            for tool in connected
        ]
    }

@router.post("/connect")
def connect_tool(payload: ToolConnect, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    tool_info = next((t for t in AVAILABLE_TOOLS if t["id"] == payload.tool_id), None)
    if not tool_info:
        raise HTTPException(status_code=404, detail="Tool not found")

    existing = db.query(ConnectedTool).filter(
        ConnectedTool.user_id == current_user.id,
        ConnectedTool.tool_id == payload.tool_id
    ).first()

    if existing:
        raise HTTPException(status_code=400, detail="Tool already connected")

    new_tool = ConnectedTool(
        user_id=current_user.id,
        tool_id=tool_info["id"],
        tool_name=tool_info["name"],
        status="connected",
        category=tool_info.get("category", "")
    )
    db.add(new_tool)
    db.commit()
    db.refresh(new_tool)

    return {
        "id": new_tool.id,
        "tool_id": new_tool.tool_id,
        "tool_name": new_tool.tool_name,
        "status": new_tool.status,
        "category": new_tool.category
    }

@router.delete("/{tool_id}")
def disconnect_tool(tool_id: str, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    tool = db.query(ConnectedTool).filter(
        ConnectedTool.user_id == current_user.id,
        ConnectedTool.tool_id == tool_id
    ).first()

    if not tool:
        raise HTTPException(status_code=404, detail="Connected tool not found")

    db.delete(tool)
    db.commit()
    return {"message": "Tool disconnected successfully"}
