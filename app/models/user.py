from pydantic import BaseModel
from datetime import datetime, timezone
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base

class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    user_id: Mapped[str] = mapped_column(unique=True)
    name: Mapped[str | None] = mapped_column(nullable=True)
    user_type: Mapped[str] = mapped_column(nullable=False)
    createdAt: Mapped[datetime] = mapped_column(default=lambda: datetime.now(timezone.utc))
    updatedAt: Mapped[datetime] = mapped_column(default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    def __repr__(self) -> str:
        return (
            f"<User(id={self.id}, user_id={self.user_id}, name={self.name}, "
            f"user_type={self.user_type}, createdAt={self.createdAt}, updatedAt={self.updatedAt})>"
        )
    

class UserSubFields(BaseModel):
    id: int
    user_id: str
    name: str | None
    user_type: str