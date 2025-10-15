from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from app.database import Base

class ConnectedTool(Base):
    __tablename__ = "connected_tools"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    tool_id = Column(String, nullable=False)
    tool_name = Column(String, nullable=False)
    status = Column(String, default="connected")
    category = Column(String, nullable=True)
