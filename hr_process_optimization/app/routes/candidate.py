from fastapi import FastAPI, UploadFile, File, Depends
from fastapi import APIRouter, HTTPException
from app.utils.resume_parser import ResumeExtractor
from app.schemas.schemas import Resume
import os
import sqlite3
from app.utils.database import SessionLocal, engine
from app.models.candidate import Resume as ResumeModel
from app.utils.crud import add_resume
from sqlalchemy.orm import Session




# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

router = APIRouter()

extractor = ResumeExtractor()

ResumeModel.metadata.create_all(bind=engine)

@router.post("/upload_resume/")
async def upload_resume(file: UploadFile = File(...), user_id: int = None, db: Session = Depends(get_db)):
    try:
        resume_bytes = await file.read()
        resume_path = f"resumes/{file.filename}"
        os.makedirs(os.path.dirname(resume_path), exist_ok=True)
        
        with open(resume_path, "wb") as f:
            f.write(resume_bytes)

        resume_data = extractor.process_resume(resume_path)
        # assing user_id to resume_data
        resume_data["user_id"] = user_id
        resume_data["resume_path"] = resume_path

        resume = add_resume(db, resume_data)

        return {"message": "Resume uploaded and processed successfully."}
    except Exception as e:
        return {"error": str(e)}

