from fastapi import APIRouter, HTTPException, Depends, Body
from fastapi.responses import JSONResponse
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
import jwt
from motor.motor_asyncio import AsyncIOMotorClient
from passlib.context import CryptContext
import os

# Create a router
router = APIRouter()

# Database setup (MongoDB example)
client = AsyncIOMotorClient(os.getenv("MONGO_URI"))
db = client.my_database
users_collection = db.users

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Secret key
JWT_SECRET = os.getenv("JWT_KEY", "mysecretkey")

# Models
class SignupRequest(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=4, max_length=20)
    name: str = Field(..., min_length=1)

class UserResponse(BaseModel):
    id: str
    email: str
    name: str

# Utility functions
def create_jwt(user_id: str, email: str) -> str:
    payload = {"id": user_id, "email": email}
    return jwt.encode(payload, JWT_SECRET, algorithm="HS256")

# Routes
@router.post("/auth-fastapi/signup", response_model=UserResponse)
async def signup(signup_data: SignupRequest = Body(...)):
    # Check if user already exists
    existing_user = await users_collection.find_one({"email": signup_data.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="Email in use")

    # Hash password
    hashed_password = pwd_context.hash(signup_data.password)

    # Create new user
    new_user = {
        "email": signup_data.email,
        "password": hashed_password,
        "name": signup_data.name,
    }
    result = await users_collection.insert_one(new_user)

    # Generate JWT token
    user_jwt = create_jwt(str(result.inserted_id), signup_data.email)

    # Mock session (store JWT as an example)
    response = UserResponse(id=str(result.inserted_id), email=signup_data.email, name=signup_data.name)
    headers = {"Authorization": f"Bearer {user_jwt}"}
    return JSONResponse(content=response.dict(), headers=headers)