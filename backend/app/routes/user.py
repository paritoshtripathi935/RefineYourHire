# app/routes/user.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.app.schemas import schemas
from backend.app.utils import crud
from backend.app.utils.database import get_db
from backend.app.utils.security import get_current_active_user

router = APIRouter()

@router.put("/users/me/", response_model=schemas.User)
def user_update_own_record(user_update: schemas.UserUpdate, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_active_user)):
    db_user = crud.update_user_self(db, current_user, user_update)
    return db_user
