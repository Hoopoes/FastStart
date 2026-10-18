from typing import Literal

from app.auth.hashing_service import verify_password
from app.auth.models import UserAuth
from app.models.user import User
from app.services.dummy_data import USERS


def _find(user_id: int) -> dict[str, int | str] | None:
    return next((u for u in USERS if u["id"] == user_id), None)


def _find_user_by_email(email: str) -> dict | None:
    email = email.lower()
    return next((u for u in USERS if u["email"].lower() == email), None)


def _email_taken(email: str, exclude_id: int | None = None) -> bool:
    return any(
        u["email"].lower() == email.lower() and u["id"] != exclude_id for u in USERS
    )


def fetch_by_id(user_id: int) -> User | None:
    user = _find(user_id)
    return User.model_validate(user) if user else None


def _filter_users(
    role: Literal["admin", "member"] | None,
    active: bool | None,
    search: str | None,
) -> list[dict]:
    users = USERS

    if role is not None:
        users = [u for u in users if u["role"] == role]

    if active is not None:
        users = [u for u in users if u["active"] == active]

    if search:
        needle = search.lower()
        users = [
            u
            for u in users
            if needle in u["name"].lower() or needle in u["email"].lower()
        ]

    return users


def fetch_all(
    page: int,
    limit: int,
    role: Literal["admin", "member"] | None,
    active: bool | None,
    search: str | None,
) -> tuple[list[User], int]:
    """Return one page of users plus the total number of matches."""
    matched = _filter_users(role, active, search)

    start = (page - 1) * limit
    page_items = matched[start : start + limit]

    return [User.model_validate(u) for u in page_items], len(matched)


def create(
    name: str,
    email: str,
    hashed_password: str,
    role: Literal["admin", "member"] = "member",
) -> User:
    if _email_taken(email):
        raise ValueError("A user with this email already exists.")

    max_id: int = max((u["id"] for u in USERS), default=0)

    user = {
        "id": max_id + 1,
        "name": name,
        "email": email,
        "hashed_password": hashed_password,
        "role": role,
        "active": True,
    }
    USERS.append(user)

    return User.model_validate(user)


def update(user_id: int, changes: dict) -> User | None:
    """Used by both PATCH (partial dict) and PUT (full dict).
    Returns None if the user doesn't exist."""
    user = _find(user_id)
    if user is None:
        return None

    new_email = changes.get("email")
    if new_email and _email_taken(new_email, exclude_id=user_id):
        raise ValueError("A user with this email already exists.")

    user.update(changes)
    return User.model_validate(user)


def delete(user_id: int) -> bool:
    user = _find(user_id)
    if user is None:
        return False
    USERS.remove(user)
    return True


def authenticate_user(email: str, password: str) -> UserAuth | None:
    user = _find_user_by_email(email)
    if user is None or not user["active"]:
        return None
    if not verify_password(password, user["hashed_password"]):
        return None
    return UserAuth(email=user["email"], role=user["role"])


def get_user(email: str) -> UserAuth | None:
    user = _find_user_by_email(email)
    return UserAuth(email=user["email"], role=user["role"]) if user else None