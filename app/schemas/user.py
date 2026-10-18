from typing import Literal

from pydantic import BaseModel, EmailStr, Field, model_validator

from app.models.user import User

Role = Literal["admin", "member"]


class CreateUserDto(BaseModel):
    tracking_id: str | None = None
    name: str = Field(..., min_length=2, max_length=30, description="User's full name")
    email: EmailStr = Field(..., description="User's email address")
    password: str = Field(
        ..., min_length=8, max_length=128, description="User's password"
    )
    role: Role = "member"


class ReplaceUserDto(BaseModel):
    """PUT: every field is required (full replacement)."""

    name: str = Field(..., min_length=2, max_length=30)
    email: EmailStr
    role: Role
    active: bool


class UpdateUserDto(BaseModel):
    """PATCH: every field is optional, but at least one must be sent."""

    name: str | None = Field(None, min_length=2, max_length=30)
    role: Role | None = None
    active: bool | None = None

    @model_validator(mode="after")
    def at_least_one_field(self):
        if not self.model_fields_set:
            raise ValueError("At least one field must be provided.")
        return self


class UsersDto(BaseModel):
    users: list[User]
    page: int
    limit: int
    total: int
    pages: int