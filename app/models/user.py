from typing import Literal

from pydantic import BaseModel, EmailStr


class User(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: Literal["admin", "member"]
    active: bool