from typing import List, Optional
from pydantic import BaseModel
from backend.app.utils.database import Base
from sqlalchemy import create_engine, Column, Integer, String
import uuid

class Resume(Base):
    __tablename__ = 'resumes'
    
    user_id = Column(Integer)
    education = Column(String)
    experience = Column(String)
    skills = Column(String)
    projects = Column(String)
    resume_path = Column(String)
    name = Column(String)
    email = Column(String)
    resume_id = Column(String, primary_key=True, default=str(uuid.uuid4()), unique=True)
