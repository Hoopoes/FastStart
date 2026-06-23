import jwt
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer


from config import CONFIG
from app.auth.models import TokenData
import app.errors.error as http_error
from app.auth.user_auth import get_user


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
        username = payload.get("sub")
        if username is None:
            raise http_error.InvalidCredentials()
        token_data = TokenData(username=username)

        user = get_user(username=token_data.username)
        if user is None:
            raise http_error.InvalidCredentials()
        return user

    except jwt.ExpiredSignatureError:
        raise http_error.TokenExpired()
    except jwt.InvalidTokenError:
        raise http_error.InvalidToken()