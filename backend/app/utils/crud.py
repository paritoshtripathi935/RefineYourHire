from sqlalchemy.orm import Session
import pyotp

from backend.app.models import user_model as models
from backend.app.models import candidate as candidate_models
from backend.app.schemas import schemas
from backend.app.utils.security import pwd_context


async def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


async def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


async def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


async def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


async def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = pwd_context.hash(user.password)
    db_user = models.User(
        email=user.email,
        username=user.username,
        full_name=user.full_name,
        hashed_password=hashed_password,
        otp_secret=pyotp.random_base32(),
        role=user.role
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

async def update_user_self(db: Session, current_user: schemas.User, user_update: schemas.UserUpdate):
    db_user = get_user(db, current_user.id)
    db_user.email = user_update.email
    db_user.username = user_update.username
    db_user.full_name = user_update.full_name
    db_user.hashed_password = pwd_context.hash(user_update.password)
    db.commit()
    db.refresh(db_user)
    return db_user


# add resume to resumes table
async def add_resume(db: Session, resume: schemas.Resume):
    db_resume = candidate_models.Resume(
        user_id=resume.get("user_id"),
        education=resume.get("education"),
        experience=resume.get("experience"),
        skills=resume.get("skills"),
        projects=resume.get("projects"),
        resume_path=resume.get("resume_path"),
        name=resume.get("name"),
        email=resume.get("email"),
        resume_id=resume.get("resume_id")
    )
    # convert list to string
    db_resume.education = ','.join(db_resume.education)
    db_resume.experience = ','.join(db_resume.experience)
    db_resume.skills = ','.join(db_resume.skills)
    db_resume.projects = ','.join(db_resume.projects)

    db.add(db_resume)
    db.commit()
    db.refresh(db_resume)
    return db_resume


async def get_resume(db: Session, user_id: int) -> bool:
    check = db.query(candidate_models.Resume).filter(candidate_models.Resume.user_id == user_id).first()

    if check:
        return True
    else:
        return False
