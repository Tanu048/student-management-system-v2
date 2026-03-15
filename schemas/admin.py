from pydantic import BaseModel, Field
from typing import Optional

class Admin(BaseModel):
    name: str
    department: str
    email: str
    username: str
    password: str
    admin_key: str = Field(..., min_length=8)

class AdminLogin(BaseModel):
    username: str
    password: str

class AdminResponse(BaseModel):
    id : int    
    name: str
    department: str
    username: str
    email: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: Optional[str] = None 
 
class TokenData(BaseModel):
    user_id: Optional[int] = None