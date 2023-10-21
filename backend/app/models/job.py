from typing import List, Optional
from pydantic import BaseModel
from backend.app.utils.database import Base
from sqlalchemy import create_engine, Column, Integer, String

class Jobs(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    job_name = Column(String)
    job_description = Column(String)