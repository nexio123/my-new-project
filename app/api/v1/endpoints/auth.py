from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from typing import Any

from ....schemas.auth import UserAuth, UserCreate, UserResponse, Token
from ....core.security import (
    create_access_token,
    create_refresh_token,
    get_password_hash,
    verify_password
)
from ....core.config import settings
from ....core.database import get_db

router = APIRouter()

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserCreate, db=Depends(get_db)) -> Any:
    # Check if user already exists
    existing_user = await db.users.find_one({"email": user_data.email})
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create new user
    user_dict = user_data.model_dump()
    user_dict["password"] = get_password_hash(user_data.password)
    user_dict["is_active"] = True
    
    result = await db.users.insert_one(user_dict)
    user_dict["id"] = str(result.inserted_id)
    
    return user_dict

@router.post("/login", response_model=Token)
async def login(db=Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()) -> Any:
    user = await db.users.find_one({"email": form_data.username})
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    
    if not verify_password(form_data.password, user["password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    
    return {
        "access_token": create_access_token(user["_id"]),
        "refresh_token": create_refresh_token(user["_id"]),
        "token_type": "bearer"
    }

@router.post("/refresh", response_model=Token)
async def refresh_token(token: str, db=Depends(get_db)) -> Any:
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        token_data = TokenPayload(**payload)
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )
    
    user = await db.users.find_one({"_id": token_data.sub})
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )
    
    return {
        "access_token": create_access_token(user["_id"]),
        "refresh_token": create_refresh_token(user["_id"]),
        "token_type": "bearer"
    }