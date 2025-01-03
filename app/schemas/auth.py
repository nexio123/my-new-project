from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional
import re

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str

class TokenPayload(BaseModel):
    sub: Optional[str] = None

class UserAuth(BaseModel):
    email: EmailStr = Field(..., description="User's email address")
    password: str = Field(..., min_length=8, description="User's password")

    @field_validator('password')
    def validate_password(cls, v):
        if not re.search(r'[A-Z]', v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not re.search(r'[a-z]', v):
            raise ValueError('Password must contain at least one lowercase letter')
        if not re.search(r'\d', v):
            raise ValueError('Password must contain at least one number')
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', v):
            raise ValueError('Password must contain at least one special character')
        return v

class UserCreate(UserAuth):
    full_name: str = Field(
        ..., 
        min_length=2, 
        max_length=100,
        pattern=r'^[a-zA-Z\s-]+$',
        description="User's full name"
    )

    @field_validator('full_name')
    def validate_full_name(cls, v):
        if len(v.strip().split()) < 2:
            raise ValueError('Full name must include both first and last name')
        return v

class UserResponse(BaseModel):
    id: str
    email: EmailStr
    full_name: str
    is_active: bool

    class Config:
        from_attributes = True