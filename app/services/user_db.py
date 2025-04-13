import prisma
from typing import Optional
from prisma.models import User
from prisma.partials import UserSubFields
from app.core.database import prisma_client


async def create(user_id: str, name: str, user_type: str):
    try:
        await prisma_client.user.create(
            data={
                "name":name,
                "user_id": user_id,
                "user_type": user_type
            }
        )
    except prisma.errors.UniqueViolationError:
        raise ValueError("The user already exists.")
    
async def delete(user_id: str) -> Optional[User]:
    user = await prisma_client.user.delete(
        where={
            "user_id": user_id,
        }
    )
    return user
    
async def fetch_all() -> list[UserSubFields]:
    return await UserSubFields.prisma().find_many()