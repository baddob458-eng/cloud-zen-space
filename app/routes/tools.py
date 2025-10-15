from fastapi import APIRouter

router = APIRouter(prefix="/api/tools", tags=["tools"])

@router.get("/list")
def list_tools():
    # front-end reads this to show curated tools
    return {"tools": [
        {"id": "chatgpt", "name": "ChatGPT"},
        {"id": "canva", "name": "Canva"},
        {"id": "zoom", "name": "Zoom"}
    ]}
