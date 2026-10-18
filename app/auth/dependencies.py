from typing import Annotated

import jwt
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

import app.errors.error as http_error
from app.auth.models import TokenData, UserAuth
from app.services.user_db import get_user
from config import CONFIG

# OAuth2 tokenUrl must match the auth login endpoint (update this if auth API route changes)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/token")


async def verify_access_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(
            token,
            CONFIG.auth_secret_key,
            algorithms=[CONFIG.auth_algorithm],
        )
        if payload.get("type") != "access":
            raise http_error.InvalidTokenType(token_type="access")
        email = payload.get("sub")
        if email is None:
            raise http_error.InvalidCredentials()
        token_data = TokenData(email=email)

        user = get_user(token_data.email)
        if user is None:
            raise http_error.InvalidCredentials()
        return user

    except jwt.ExpiredSignatureError:
        raise http_error.TokenExpired()
    except jwt.InvalidTokenError:
        raise http_error.InvalidToken()


async def require_admin(
    current_user: Annotated[UserAuth, Depends(verify_access_token)],
) -> UserAuth:
    if current_user.role != "admin":
        raise http_error.AdminPrivilegeRequired()
    return current_user