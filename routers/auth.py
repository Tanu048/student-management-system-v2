from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from pwdlib import PasswordHash
import jwt
from datetime import datetime, timedelta
import os

from schemas.admin import Admin, AdminLogin, Token, AdminResponse
from storage_handler.db_handler.db_handler import StudentDB
from storage_handler.db_handler.db_model import AdminDBModel

router = APIRouter()

hasher=PasswordHash.recommended()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

@router.post("/register")
def register(user: Admin, db:Session = Depends(StudentDB.get_db)):
    try:
        existing_user = db.query(AdminDBModel).filter_by(username=user.username).first()
        if existing_user:
            return {"message": "Username already exists"}
        existing_user = db.query(AdminDBModel).filter_by(email=user.email).first()
        if existing_user:
            return {"message": "Email already exists"}
        new_user = AdminDBModel(
            name=user.name,
            department=user.department,
            email=user.email,
            username=user.username,
            password=hasher.hash(user.password),
            admin_key=user.admin_key
        )
        db.add(new_user)
        db.commit()
        return {"message": "User registered successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/login", response_model=Token, status_code=status.HTTP_200_OK)
def login(data: AdminLogin, db: Session = Depends(StudentDB.get_db)) -> dict:
    """Login with username and password to receive JWT token."""
    user = db.query(AdminDBModel).filter(AdminDBModel.username == data.username).first()
    if not user or not hasher.verify(data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    expire_time = datetime.now() + timedelta(minutes=int(os.getenv("EXPIRE_MINUTES")))
    if not expire_time:
        raise RuntimeError("Environment variable is not set")
    token = jwt.encode(
        {"username": user.username, "role": user.role, "exp": expire_time},
        os.getenv("SECRET_KEY"),
        algorithm=os.getenv("ALGORITHM"),
    )
    if not token:
        raise RuntimeError("Environment variable is not set")

    return {
        "access_token": token,
        "token_type": "bearer",
        "expires_in": expire_time.isoformat(),
    }

@router.get("/is_auth", response_model=AdminResponse, status_code=status.HTTP_200_OK) 
def is_auth(token: str = Depends(oauth2_scheme), db: Session = Depends(StudentDB.get_db)):

    try:
        payload = jwt.decode(
            token, os.getenv("SECRET_KEY"), algorithms=[os.getenv("ALGORITHM")]
        )
        if not payload:
            raise RuntimeError("Environment variable is not set")

        username = payload.get("username")

        user = db.query(AdminDBModel).filter(AdminDBModel.username == username).first()

        if not user:
            raise HTTPException(status_code=401, detail="User not found")

        return user

    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")

    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")