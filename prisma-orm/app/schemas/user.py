from typing import Literal
from pydantic import BaseModel, Field
from prisma.partials import UserSubFields

from app.schemas.base import BaseResponseDto



class CreateUserDto(BaseModel):
    user_type: Literal["BUYER", "SELLER"]
    name: str = Field(..., max_length=30, description="user's name")
    user_id: str = Field(..., max_length=10, description="user id assignment")

class UsersDto(BaseResponseDto):
    users: list[UserSubFields]