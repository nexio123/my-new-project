from pydantic import BaseModel, EmailStr, Field, validator
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
    password: str = Field(
        ...,
        min_length=8,
        max_length=100,
        description="Password must be between 8 and 100 characters"
    )

    @validator('password')
    def password_complexity(cls, v):
        if not re.search(r'[A-Z]', v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not re.search(r'[a-z]', v):
            raise ValueError('Password must contain at least one lowercase letter')
        if not re.search(r'\d', v):
            raise ValueError('Password must contain at least one digit')
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', v):
            raise ValueError('Password must contain at least one special character')
        return v

class UserCreate(UserAuth):
    full_name: str = Field(
        ...,
        min_length=2,
        max_length=100,
        description="User's full name must be between 2 and 100 characters"
    )

    @validator('full_name')
    def validate_full_name(cls, v):
        if not v.strip():
            raise ValueError('Full name cannot be empty or just whitespace')
        if not all(part.isalpha() or part.isspace() for part in v):
            raise ValueError('Full name can only contain letters and spaces')
        return v.strip()

class UserResponse(BaseModel):
    id: str
    email: EmailStr
    full_name: str
    is_active: bool

    class Config:
        from_attributes = True