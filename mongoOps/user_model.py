from bson import ObjectId
from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List
from enum import Enum
from pydantic.json import ENCODERS_BY_TYPE

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
    def __get_pydantic_json_schema__(cls, schema):
        schema.update(type="string")
        return schema

# Register the custom encoder for PyObjectId
ENCODERS_BY_TYPE[ObjectId] = str

# Enums
class UserRole(str, Enum):
    ADMIN = "ADMIN"
    USER = "USER"

# User model
class User(BaseModel):
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
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

class UserResponse(BaseModel):
    id: str
    email: str
    name: str

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
