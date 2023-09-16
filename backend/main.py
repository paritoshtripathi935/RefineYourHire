# code originally from - https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/
from datetime import datetime, timedelta
from typing import Optional

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from pydantic import BaseModel

from sqlalchemy.orm import Session
from app.utils import crud
from app.models import user_model as models
from app.schemas import schemas
from app.utils.database import SessionLocal, engine

from app.utils.security import pwd_context

models.Base.metadata.create_all(bind=engine)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
app = FastAPI()

# import routes from routes folder
from app.routes.candidate import router as candidate_router
from app.routes.auth import router as auth_router
from app.routes.job import router as job_router

app.include_router(candidate_router, tags=["Candidate"], prefix="/candidate")
app.include_router(auth_router, tags=["User Authentication"], prefix="/auth")
app.include_router(job_router, tags=["Job"], prefix="/job")

