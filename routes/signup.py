from fastapi import APIRouter, HTTPException, Depends, Body
from fastapi.responses import JSONResponse
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
import jwt
import os

from mongoOps.operations import create_user, get_user_by_email
from mongoOps.user_model import User, UserResponse
from main import get_database  # Import the get_database dependency

# Create a router
router = APIRouter()

# Secret key
JWT_SECRET = os.getenv("JWT_KEY", "mysecretkey")

# Models
class SignupRequest(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=4, max_length=20)
    name: str = Field(..., min_length=1)

# Utility functions
def create_jwt(user_id: str, email: str) -> str:
    payload = {"id": user_id, "email": email}
    return jwt.encode(payload, JWT_SECRET, algorithm="HS256")

# Routes
@router.post("/auth-fastapi/signup", response_model=UserResponse)
async def signup(signup_data: SignupRequest = Body(...), db=Depends(get_database)):
    # Check if user already exists
    existing_user = await get_user_by_email(signup_data.email, db)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email in use")

    # Create new user
    new_user = User(
        email=signup_data.email,
        password=signup_data.password,
        name=signup_data.name
    )
    created_user = await create_user(new_user, db)

    # Generate JWT token
    user_jwt = create_jwt(str(created_user.id), created_user.email)

    # Mock session (store JWT as an example)
    response = UserResponse(id=str(created_user.id), email=created_user.email, name=created_user.name)
    headers = {"Authorization": f"Bearer {user_jwt}"}
    return JSONResponse(content=response.dict(), headers=headers)