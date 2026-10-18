from datetime import UTC, datetime, timedelta
from typing import Literal

import jwt

from config import CONFIG


def create_token(
    data: dict,
    token_type: Literal["access", "refresh"],
    expires_delta: timedelta,
) -> str:
    to_encode = data.copy()

    expire = datetime.now(UTC) + expires_delta

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