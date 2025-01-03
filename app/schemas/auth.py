from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str

class TokenPayload(BaseModel):
    sub: Optional[str] = None

class UserAuth(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8)

class UserCreate(UserAuth):
    full_name: str = Field(..., min_length=1, max_length=100)

class UserResponse(BaseModel):
    id: str
    email: EmailStr
    full_name: str
    is_active: bool

    class Config:
        from_attributes = True