from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from pwdlib import PasswordHash
import jwt
from datetime import datetime, timedelta, timezone
import os

from schemas.admin import Admin, AdminLogin, Token, AdminResponse
from storage_handler.db_handler.db_handler import StudentDB
from storage_handler.db_handler.db_model import AdminDBModel

router = APIRouter()

hasher = PasswordHash.recommended()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def _get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(StudentDB.get_db),
) -> AdminDBModel:
    secret = os.getenv("SECRET_KEY")
    algorithm = os.getenv("ALGORITHM", "HS256")
    if not secret:
        raise RuntimeError("SECRET_KEY is not configured")
    try:
        payload = jwt.decode(token, secret, algorithms=[algorithm])
        username = payload.get("username")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        user = db.query(AdminDBModel).filter(AdminDBModel.username == username).first()
        if not user:
            raise HTTPException(status_code=401, detail="User not found")
        return user
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

@router.post("/register")
def register(user: Admin, db: Session = Depends(StudentDB.get_db)):
    try:
        existing_user = db.query(AdminDBModel).filter_by(username=user.username).first()
        if existing_user:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Username already exists")
        
        existing_user = db.query(AdminDBModel).filter_by(email=user.email).first()
        if existing_user:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User with this email already exists")
        
        if user.role == "admin":
            if not user.admin_key:
                raise HTTPException(status_code=400, detail="admin_key is required for admin role")
            expected_key = os.getenv("ADMIN_KEY")
            if not expected_key or user.admin_key != expected_key:
                raise HTTPException(status_code=403, detail="Invalid admin key")
            
        new_user = AdminDBModel(
            name=user.name,
            department=user.department,
            email=user.email,
            username=user.username,
            password=hasher.hash(user.password),
            role=user.role,
        )
        db.add(new_user)
        db.commit()
        return {"message": "User registered successfully"}
    except HTTPException:
        raise              
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
    secret = os.getenv("SECRET_KEY")
    algorithm = os.getenv("ALGORITHM", "HS256")
    if not secret:
        raise RuntimeError("SECRET_KEY environment variable is not set")

    expire_time = datetime.now(timezone.utc) + timedelta(minutes=int(os.getenv("EXPIRE_MINUTES", "60")))
    token = jwt.encode(
        {"username": user.username, "role": user.role, "exp": expire_time},
        secret,
        algorithm=algorithm,
    )
    return {"access_token": token, "token_type": "bearer", "expires_in": expire_time.isoformat()}

@router.get("/is_auth", response_model=AdminResponse, status_code=status.HTTP_200_OK)
def is_auth(current_user: AdminDBModel = Depends(_get_current_user)):
    return current_user


def require_role(*roles: str):
    def role_checker(current_user: AdminDBModel = Depends(_get_current_user)) -> AdminDBModel:
        if current_user.role not in roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access denied. Required role(s): {', '.join(roles)}",
            )
        return current_user
    return role_checker