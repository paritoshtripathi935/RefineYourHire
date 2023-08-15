from typing import List, Optional
from pydantic import BaseModel
from app.utils.database import Base
from sqlalchemy import create_engine, Column, Integer, String

class Resume(Base):
    __tablename__ = 'resumes'
    
    user_id = Column(Integer, primary_key=True, autoincrement=True)
    education = Column(String)
    experience = Column(String)
    skills = Column(String)
    projects = Column(String)
    resume_path = Column(String)
    name = Column(String)
    email = Column(String)
