from typing import Annotated, Literal

from fastapi import APIRouter, Depends, Path, Query, Response, status

import app.errors.error as http_error
from app.auth.dependencies import require_admin, verify_access_token
from app.auth.hashing_service import hash_password
from app.auth.models import UserAuth
from app.models.user import User
from app.schemas.base import BaseResponseDto
from app.schemas.user import CreateUserDto, ReplaceUserDto, UpdateUserDto, UsersDto
from app.services import user_db
from app.services.user_service import _validate_name
from app.utils.log_handler import set_log_context
from app.utils.logger import LOG

user_router = APIRouter()


@user_router.get("")
async def list_users(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    role: Literal["admin", "member"] | None = Query(None),
    active: bool | None = Query(None),
    search: str | None = Query(None),
) -> UsersDto:
    users, total = user_db.fetch_all(page, limit, role, active, search)
    LOG.debug("user list", extra={"obj": [u.model_dump() for u in users]})
    return UsersDto(
        users=users,
        page=page,
        limit=limit,
        total=total,
        pages=(total + limit - 1) // limit,
    )


@user_router.get("/{user_id}")
async def get_user(user_id: int = Path(...)) -> User:
    user = user_db.fetch_by_id(user_id)
    if not user:
        raise http_error.UserNotExist()
    return user


@user_router.post("", status_code=status.HTTP_201_CREATED)
async def create_user(req: CreateUserDto) -> BaseResponseDto:
    if req.tracking_id:
        set_log_context(tracking_id=req.tracking_id)

    _validate_name(req.name)

    try:
        LOG.info(f"Create user {req.name}")
        user = user_db.create(
            req.name, req.email, hash_password(req.password), req.role
        )
        LOG.debug("User created", extra={"obj": user.model_dump()})
    except ValueError:
        raise http_error.UserIDAlreadyExist()

    return BaseResponseDto(code="SUCCESS", message="User Successfully Created")


@user_router.patch("/{user_id}")
async def patch_user(
    _: Annotated[UserAuth, Depends(verify_access_token)],
    req: UpdateUserDto,
    user_id: int = Path(...),
) -> User:
    set_log_context(user_id=str(user_id))
    changes = req.model_dump(exclude_unset=True)
    _validate_name(changes.get("name"))

    try:
        user = user_db.update(user_id, changes)
    except ValueError:
        raise http_error.UserIDAlreadyExist()

    if user is None:
        raise http_error.UserNotExist()
    return user


@user_router.put("/{user_id}")
async def replace_user(
    current_user: Annotated[UserAuth, Depends(require_admin)],
    req: ReplaceUserDto,
    user_id: int = Path(...),
) -> User:
    set_log_context(user_id=str(user_id))

    target = user_db.fetch_by_id(user_id)
    if target is None:
        raise http_error.UserNotExist()
    if target.email.lower() == current_user.email.lower():
        raise http_error.CannotReplaceSelf()
    if target.role == "admin":
        raise http_error.CannotReplaceAdmin()

    _validate_name(req.name)

    try:
        user = user_db.update(user_id, req.model_dump())
    except ValueError:
        raise http_error.UserIDAlreadyExist()

    if user is None:
        raise http_error.UserNotExist()
    return user


@user_router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    current_user: Annotated[UserAuth, Depends(require_admin)],
    user_id: int = Path(...),
) -> Response:
    set_log_context(user_id=str(user_id))

    target = user_db.fetch_by_id(user_id)
    if target is None:
        raise http_error.UserNotExist()
    if target.email.lower() == current_user.email.lower():
        raise http_error.CannotDeleteSelf()
    if target.role == "admin":
        raise http_error.CannotDeleteAdmin()

    user_db.delete(user_id)

    LOG.info(f"User {user_id} deleted by admin {current_user.email}")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
