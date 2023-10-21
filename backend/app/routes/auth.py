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
from fastapi import APIRouter
from dotenv import load_dotenv
import os


models.Base.metadata.create_all(bind=engine)
router = APIRouter()
load_dotenv()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
async def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

async def get_password_hash(password):
    return pwd_context.hash(password)

async def get_user(db: Session, username: str):
    return await crud.get_user_by_username(db, username)

async def authenticate_user(db: Session, username: str, password: str):
    """
    Authenticate a user by checking their credentials.

    :param db: Database session.
    :param username: User's username.
    :param password: User's password.
    :return: User object if authentication succeeds, False otherwise.
    """
    user = await get_user(db, username)
    if not user:
        return False
    if await verify_password(password, user.hashed_password) is False:
        print("password is false")
        return False
    
    return user


async def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):

    """
    Create an access token for a user.

    :param data: Dictionary containing user data to be encoded in the token.
    :param expires_delta: Optional timedelta for token expiration.
    :return: Encoded JWT access token.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme),
                     db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = schemas.TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
        current_user: schemas.User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


async def get_current_active_admin_user(
        current_user: schemas.User = Depends(get_current_active_user), ):
    if current_user.role != schemas.Role.admin:
        raise HTTPException(status_code=400,
                            detail="User has insufficient permissions")
    return current_user


@router.post("/token", response_model=schemas.Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(),
                           db: Session = Depends(get_db)):
    """
    Get an access token for a user based on their username and password.

    :param form_data: OAuth2PasswordRequestForm containing username and password.
    :param db: Database session.
    :return: Token response containing the access token.
    """
    user = await authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = await create_access_token(data={"sub": user.username},
                                       expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/users/me/", response_model=schemas.User)
async def read_users_me(
        current_user: schemas.User = Depends(get_current_active_user)):
    return current_user


@router.put("/users/me/", response_model=schemas.User)
async def user_update_own_record(user_update: schemas.UserUpdate, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_active_user)):
    db_user = await crud.update_user_self(db, current_user, user_update)
    return db_user
    

@router.get("/users/{user_id}", response_model=schemas.User)
async def get_user_by_id(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_active_admin_user)):
    db_user = await crud.get_user(db, user_id)
    return db_user


@router.post("/users/", response_model=schemas.User)
async def create_new_user(
    user: schemas.UserCreate,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_active_admin_user)):
    db_user = await crud.create_user(db, user)
    return db_user


# make a signup api endpoint that doesnot rqeuire authentication
@router.post("/signup/", response_model=schemas.User)
async def signup(
    user: schemas.UserCreate,
    db: Session = Depends(get_db)):
    """
    Signup endpoint that does not require authentication.

    :param user: UserCreate containing username, password, and role.
    :param db: Database session.
    :return: User response containing the created user.
    """

    db_user = await crud.create_user(db, user)
    return db_user

# login api endpoint that doesnot require authentication

@router.post("/login/", response_model=schemas.Token)
async def login(payload: models.LoginPayload, db: Session = Depends(get_db)):
    """
    Login endpoint that does not require authentication.

    :param payload: LoginPayload containing username and password.
    :param db: Database session.
    :return: Token response containing the access token.
    """


    # check if user exists
    user = await authenticate_user(db, payload.username, payload.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password")
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = await create_access_token(data={"sub": user.username},
                                       expires_delta=access_token_expires)
    
    return {"access_token": access_token, "token_type": "bearer"}
