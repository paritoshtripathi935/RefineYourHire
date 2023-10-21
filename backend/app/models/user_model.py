from sqlalchemy import Boolean, Column, Integer, String, Enum
from backend.app.utils.database import Base
from backend.app.schemas.schemas import Role


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    full_name = Column(String)
    hashed_password = Column(String)
    otp_secret = Column(String)
    disabled = Column(Boolean, default=False)
    role = Column(Enum(Role))

from pydantic import BaseModel

class LoginPayload(BaseModel):
    username: str
    password: str