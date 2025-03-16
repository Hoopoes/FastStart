from typing import Any
from enum import StrEnum
from pydantic import BaseModel, Field
from prisma.partials import UserSubFields
from app.schema.base_schema import BaseResponse


class UserType(StrEnum):
    BUYER = "BUYER"
    SELLER = "SELLER"

class UserBase(BaseModel):
    name: str = Field(..., max_length=30, description="user's name")
    user_type: UserType

class CreateUser(UserBase):
    user_id: str = Field(..., max_length=10, description="user id assignment")

class Users(BaseResponse):
    users: list[UserSubFields]