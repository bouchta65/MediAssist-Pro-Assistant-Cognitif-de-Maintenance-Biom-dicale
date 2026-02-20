from sqlalchemy import Column,Integer,String,DateTime,Boolean
from app.core.database import Base
from datetime import datetime


class Users(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False, unique=True)
    email = Column(String, nullable=False, unique=True)
    hashed_password = Column(String, nullable=True)  
    google_id = Column(String, nullable=True, unique=True)
    is_oauth = Column(Boolean, default=False)
    role = Column(String, default="user")
    created_at = Column(DateTime, default=datetime.utcnow)