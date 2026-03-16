from pydantic import BaseModel, EmailStr, Field
from typing import Literal, Optional


class Admin(BaseModel):
    name: str
    department: str
    email: str
    username: str
    password: str = Field(..., min_length=8)
    role: Literal["admin", "viewer"] = "viewer"
    admin_key: Optional[str] = None


class AdminLogin(BaseModel):
    username: str
    password: str


class AdminResponse(BaseModel):
    id: int
    name: str
    department: str
    username: str
    email: str
    role: str

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: Optional[str] = None


class TokenData(BaseModel):
    username: Optional[str] = None
    role: Optional[str] = None