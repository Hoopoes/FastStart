from typing import Annotated
from datetime import timedelta
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm


from config import CONFIG
from app.auth.models import Token
import app.errors.error as http_error
from app.auth.jwt import create_token
from app.auth.user_auth import authenticate_user


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
        data={"sub": user.username},
        token_type="access",
        expires_delta=token_expires,
    )
    return Token(
        access_token=access_token,
        token_type="bearer",
    )