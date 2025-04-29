from pydantic import BaseModel
from datetime import datetime, timezone
from sqlalchemy.orm import DeclarativeBase, MappedAsDataclass, Mapped, mapped_column

def get_date():
    return datetime.now(timezone.utc)

class Base(DeclarativeBase, MappedAsDataclass):
    pass


# With mapped_column, use type directly; without it, use Mapped[type] annotation (for better intellisense)
class User(Base):
    __tablename__ = 'users'

    id: int = mapped_column(init=False, primary_key=True, autoincrement=True, index=True)
    user_id: str = mapped_column(unique=True)
    name: Mapped[str | None]
    user_type: Mapped[str]
    created_at: datetime = mapped_column(init=False, default=get_date)
    updated_at: datetime = mapped_column(init=False, default=get_date, onupdate=lambda: get_date)

    def __repr__(self) -> str:
        return (
            f"<User(id={self.id}, user_id={self.user_id}, name={self.name}, "
            f"user_type={self.user_type}, createdAt={self.created_at}, updatedAt={self.updated_at})>"
        )
    

class UserSubFields(BaseModel):
    id: int
    user_id: str
    name: str | None
    user_type: str