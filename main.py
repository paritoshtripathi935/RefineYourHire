# code originally from - https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/
from datetime import datetime, timedelta
from typing import Optional

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from pydantic import BaseModel

from sqlalchemy.orm import Session
from backend.app.utils import crud
from backend.app.models import user_model as models
from backend.app.schemas import schemas
from backend.app.utils.database import SessionLocal, engine
from backend.app.utils.security import pwd_context
from fastapi.responses import FileResponse
from pathlib import Path
from fastapi.staticfiles import StaticFiles

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
from backend.app.routes.candidate import router as candidate_router
from backend.app.routes.auth import router as auth_router
from backend.app.routes.job import router as job_router

app.include_router(candidate_router, tags=["Candidate"], prefix="/candidate")
app.include_router(auth_router, tags=["User Authentication"], prefix="/auth")
app.include_router(job_router, tags=["Job"], prefix="/job")

# Define the path to your 'index.html' file in the frontend folder
index_html_path = Path("frontend/index.html")
login_html_path = Path("frontend/login.html")

@app.get("/")
async def read_root():
    # Serve the 'index.html' file
    return FileResponse(index_html_path)

@app.get("/login")
async def read_login():
    return FileResponse(login_html_path)

app.mount("/static", StaticFiles(directory="frontend/static"), name="static")
