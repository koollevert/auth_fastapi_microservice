from fastapi import HTTPException
from passlib.context import CryptContext
from pydantic import BaseModel

# Define User model
class User(BaseModel):
    id: str = None
    email: str
    password: str

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Helper functions
async def get_user_by_email(email: str, db):
    user = await db["users"].find_one({"email": email})
    if user:
        return User(**user)
    return None

async def create_user(user_data: User, db):
    existing_user = await get_user_by_email(user_data.email, db)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already in use")
    
    # Hash password
    hashed_password = pwd_context.hash(user_data.password)
    user_data.password = hashed_password
    
    # Insert into MongoDB
    user_dict = user_data.dict(by_alias=True, exclude_unset=True)
    result = await db["users"].insert_one(user_dict)
    user_data.id = result.inserted_id
    return user_data

async def authenticate_user(email: str, password: str, db):
    user = await get_user_by_email(email, db)
    if user and pwd_context.verify(password, user.password):
        return user
    return None
