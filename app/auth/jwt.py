import jwt
from typing import Literal
from datetime import datetime, timedelta, timezone

from config import CONFIG


def create_token(
    data: dict,
    token_type: Literal["access", "refresh"],
    expires_delta: timedelta,
) -> str:
    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + expires_delta

    to_encode.update(
        {
            "exp": expire,
            "type": token_type,
        }
    )

    return jwt.encode(
        to_encode,
        CONFIG.auth_secret_key,
        algorithm=CONFIG.auth_algorithm,
    )