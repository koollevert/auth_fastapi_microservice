from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from enum import Enum
from bson import ObjectId

# Pydantic BSON ObjectId validation
class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")

# Enums
class UserRole(str, Enum):
    ADMIN = "ADMIN"
    USER = "USER"

# User model
class User(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id")
    email: EmailStr
    password: Optional[str]
    role: UserRole = UserRole.USER
    is_two_factor_enabled: bool = False
    two_factor_confirmation: Optional[PyObjectId]
    name: Optional[str]
    email_verified: Optional[str]
    image: Optional[str]
    accounts: List[PyObjectId] = []

    class Config:
        json_encoders = {ObjectId: str}
        allow_population_by_field_name = True

# TwoFactorConfirmation model
class TwoFactorConfirmation(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id")
    user_id: PyObjectId

    class Config:
        json_encoders = {ObjectId: str}
        allow_population_by_field_name = True

# Account model
class Account(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id")
    user_id: PyObjectId
    type: str
    provider: str
    provider_account_id: str

    class Config:
        json_encoders = {ObjectId: str}
        allow_population_by_field_name = True
