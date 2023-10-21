# make a router for hr to post a job 
# paramters are job name and job description

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi import FastAPI, UploadFile, File, Depends
from fastapi import APIRouter, HTTPException
from backend.app.schemas.schemas import JobDescription, ScreeningQuestion, ShortlistedCandidate
import os
import sqlite3
from backend.app.utils.database import SessionLocal, engine
from sqlalchemy.orm import Session
from backend.app.models.job import Jobs as JobModel


router = APIRouter()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

JobModel.metadata.create_all(bind=engine)

@router.post("/post_job/")
async def post_job(job: JobDescription, db: Session = Depends(get_db)):
    try:
        # add job to database
        return {"message": "Job posted successfully."}
    except Exception as e:
        return {"error": str(e)}

@router.post("/add_screening_question/")
async def add_screening_question(question: ScreeningQuestion, db: Session = Depends(get_db)):
    try:
        # add question to database
        return {"message": "Question added successfully."}
    except Exception as e:
        return {"error": str(e)}
    
@router.post("/shortlist_candidate/")
async def shortlist_candidate(candidate: ShortlistedCandidate, db: Session = Depends(get_db)):
    try:
        # add candidate to database
        return {"message": "Candidate shortlisted successfully."}
    except Exception as e:
        return {"error": str(e)}

