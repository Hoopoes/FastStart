import sqlalchemy
import sqlalchemy.exc
from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.models.user import UserSubFields


async def create(db: AsyncSession, user_id: str, name: str, user_type: str):
    try:
        new_user = User(
            user_id=user_id,
            name=name,
            user_type=user_type,
        )
        
        # Add and commit the new user to the database
        db.add(new_user)
        await db.commit()

        # Refresh the instance to get the user id (after insert)
        await db.refresh(new_user)
    
    except sqlalchemy.exc.IntegrityError:
        raise ValueError("The user already exists.")
    
async def delete(db: AsyncSession, user_id: str) -> Optional[User]:
    result = await db.execute(
        select(User)
        .where(User.user_id == user_id)
        .limit(1)
    )
    user = result.scalar_one_or_none()
    if user:
        await db.delete(user)
        await db.commit()
    return user
    
async def fetch_all(db: AsyncSession) -> list[UserSubFields]:
    result = await db.execute(
        select(User.id, User.user_id, User.name, User.user_type)
    )
    users = [UserSubFields.model_validate(i) for i in result.mappings().all()]
    return users