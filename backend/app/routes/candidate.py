from fastapi import UploadFile, File, Depends, HTTPException
from fastapi import APIRouter
from backend.app.utils.resume_parser import ResumeExtractor
from backend.app.utils.database import SessionLocal, engine
from backend.app.models.candidate import Resume as ResumeModel
from backend.app.utils.crud import add_resume, get_resume
from sqlalchemy.orm import Session
import uuid
import os


async def get_uuid():
    return uuid.uuid4()

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
        resume_path = f"app/resumes/{file.filename}"
        os.makedirs(os.path.dirname(resume_path), exist_ok=True)
        
        with open(resume_path, "wb") as f:
            f.write(resume_bytes)

        resume_data = await ResumeExtractor().process_resume(resume_path)

        resume_data["user_id"] = user_id
        resume_data["resume_path"] = resume_path
        resume_data["resume_id"] = str(uuid.uuid4())

        check = await get_resume(db, user_id)

        if check:
            resume = await add_resume(db, resume_data)
            return {"message": "Resume updated successfully", "resumeData": resume_data}
        
        else:
            resume = await add_resume(db, resume_data)
            return {"message": "Resume uploaded and processed successfully", "resumeData": resume_data}
    
    except Exception as e:
        return HTTPException(status_code=502, detail=str(e))
    
# apply to job
@router.post("/apply_to_job/")
async def apply_to_job(db: Session = Depends(get_db), user_id: int = None):
    try:
        # add user-id to job application
        return {"message": "Job application submitted successfully."}
    except Exception as e:
        return {"error": str(e)}