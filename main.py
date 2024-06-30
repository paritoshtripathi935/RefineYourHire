from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer
from backend.app.models import user_model as models
from backend.app.utils.database import SessionLocal, engine
from fastapi.responses import FileResponse
from pathlib import Path
from fastapi.staticfiles import StaticFiles
from backend.app.routes.candidate import router as candidate_router
from backend.app.routes.auth import router as auth_router
from backend.app.routes.job import router as job_router
import uvicorn
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

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8001)