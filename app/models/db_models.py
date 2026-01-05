from datetime import datetime
from sqlalchemy import func, DateTime
from pydantic import BaseModel, ConfigDict
from sqlalchemy.orm import DeclarativeBase, MappedAsDataclass, Mapped, mapped_column

class Base(DeclarativeBase, MappedAsDataclass):
    pass

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        init=False, primary_key=True, autoincrement=True, index=True
    )
    user_id: Mapped[str] = mapped_column(unique=True)
    name: Mapped[str | None]
    user_type: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), init=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        init=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

    def __repr__(self) -> str:
        return (
            f"<User(id={self.id}, user_id={self.user_id}, name={self.name}, "
            f"user_type={self.user_type}, createdAt={self.created_at}, updatedAt={self.updated_at})>"
        )


class UserSubFields(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: str
    name: str | None
    user_type: str
