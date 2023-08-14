from enum import Enum

from typing import List, Optional

from pydantic import BaseModel

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None

    
class Role(str, Enum):
    admin = 'admin'
    user = 'user'

class UserBase(BaseModel):
    username: str
    email: str = None
    full_name: Optional[str] = None


class UserCreate(UserBase):
    password: str
    role: Role = Role.user

class UserUpdate(UserBase):
    password: str


class User(UserBase):
    id: int
    disabled: bool = False

    class Config:
        orm_mode = True


from typing import List

class JobDescription(BaseModel):
    title: str
    description: str

class ScreeningQuestion(BaseModel):
    question: str
    importance: int

class Resume(BaseModel):
    user_id: int
    education: List[str]
    experience: List[str]
    skills: List[str]
    projects: List[str]

class ShortlistedCandidate(BaseModel):
    user_id: int
    resume_id: int

class InterviewFeedback(BaseModel):
    user_id: int
    resume_id: int
    feedback: str
