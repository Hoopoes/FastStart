from enum import StrEnum
from pydantic import BaseModel, Field

class UserType(StrEnum):
    BUYER = "BUYER"
    SELLER = "SELLER"

class UserBase(BaseModel):
    name: str = Field(..., max_length=30, description="user's name")
    user_type: UserType

class CreateUser(UserBase):
    user_id: str = Field(..., max_length=10, description="user id assignment")