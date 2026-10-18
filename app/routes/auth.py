from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

import app.errors.error as http_error
from app.auth.jwt import create_token
from app.auth.models import Token
from app.services.user_db import authenticate_user
from config import CONFIG

AUTH_ROUTER = APIRouter()


@AUTH_ROUTER.post("/token")
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise http_error.InvalidAuthentication()
    token_expires = timedelta(minutes=CONFIG.auth_access_token_expire_min)
    access_token = create_token(
        data={"sub": user.email},
        token_type="access",
        expires_delta=token_expires,
    )
    return Token(
        access_token=access_token,
        token_type="bearer",
    )