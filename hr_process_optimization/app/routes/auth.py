from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import Session
from app.utils.database import get_db
from app.utils.auth import get_password_hash
from sqlalchemy import select
from app.models.user_model import User
from app.models.user_model import UserCreate

router = APIRouter()

@router.post("/register/", response_model=User)
def register_user(user_data: UserCreate):
    db = get_db()

    # Check if user already exists
    query = select(User.username, User.email)
    results = db.session.execute(query)

    # If the user does not exist, create a new user
    hashed_password = get_password_hash(user_data.password)
    new_user = User(email=user_data.email, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
