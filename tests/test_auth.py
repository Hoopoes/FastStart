"""Authentication and token validation tests for POST /api/token."""

from datetime import timedelta

import jwt
import pytest
from conftest import (
    ADMIN_EMAIL,
    ADMIN_PASSWORD,
    INACTIVE_EMAIL,
    INACTIVE_PASSWORD,
    MEMBER_EMAIL,
    MEMBER_ID,
    MEMBER_PASSWORD,
    login,
)

from app.auth.jwt import create_token
from config import CONFIG

TOKEN_URL = "/api/token"

# PATCH is the only endpoint that is authenticated but not admin-only, which
# makes it the right probe for "is this token accepted".
PROTECTED_URL = f"/api/v1/users/{MEMBER_ID}"
PROTECTED_BODY = {"active": False}


async def test_login_returns_bearer_token(client):
    response = await client.post(
        TOKEN_URL, data={"username": ADMIN_EMAIL, "password": ADMIN_PASSWORD}
    )

    assert response.status_code == 200
    body = response.json()
    assert body["token_type"] == "bearer"
    assert body["access_token"]


async def test_login_token_carries_email_as_subject(client):
    response = await client.post(
        TOKEN_URL, data={"username": ADMIN_EMAIL, "password": ADMIN_PASSWORD}
    )
    token = response.json()["access_token"]

    payload = jwt.decode(
        token, CONFIG.auth_secret_key, algorithms=[CONFIG.auth_algorithm]
    )

    assert payload["sub"] == ADMIN_EMAIL
    assert payload["type"] == "access"


async def test_login_with_wrong_password_is_rejected(client):
    response = await client.post(
        TOKEN_URL, data={"username": ADMIN_EMAIL, "password": "wrong-password"}
    )

    assert response.status_code == 401
    assert response.json()["code"] == "INVALID_AUTHENTICATION"


async def test_login_email_is_case_insensitive(client):
    response = await client.post(
        TOKEN_URL, data={"username": ADMIN_EMAIL.upper(), "password": ADMIN_PASSWORD}
    )

    assert response.status_code == 200


async def test_inactive_user_cannot_log_in(client):
    response = await client.post(
        TOKEN_URL, data={"username": INACTIVE_EMAIL, "password": INACTIVE_PASSWORD}
    )

    assert response.status_code == 401
    assert response.json()["code"] == "INVALID_AUTHENTICATION"


async def test_missing_token_is_rejected(client):
    response = await client.patch(PROTECTED_URL, json=PROTECTED_BODY)

    assert response.status_code == 401


async def test_malformed_token_is_rejected(client):
    response = await client.patch(
        PROTECTED_URL,
        json=PROTECTED_BODY,
        headers={"Authorization": "Bearer not-a-jwt"},
    )

    assert response.status_code == 401
    assert response.json()["code"] == "INVALID_TOKEN"


async def test_expired_token_is_rejected(client):
    expired = create_token(
        data={"sub": ADMIN_EMAIL},
        token_type="access",
        expires_delta=timedelta(minutes=-1),
    )

    response = await client.patch(
        PROTECTED_URL,
        json=PROTECTED_BODY,
        headers={"Authorization": f"Bearer {expired}"},
    )

    assert response.status_code == 401
    assert response.json()["code"] == "TOKEN_EXPIRED"


async def test_refresh_token_is_rejected_as_access_token(client):
    refresh = create_token(
        data={"sub": ADMIN_EMAIL},
        token_type="refresh",
        expires_delta=timedelta(minutes=5),
    )

    response = await client.patch(
        PROTECTED_URL,
        json=PROTECTED_BODY,
        headers={"Authorization": f"Bearer {refresh}"},
    )

    assert response.status_code == 401
    assert response.json()["code"] == "INVALID_TOKEN_TYPE"


async def test_token_of_deleted_user_is_rejected(client):
    token = await login(client, MEMBER_EMAIL, MEMBER_PASSWORD)
    admin_token = await login(client, ADMIN_EMAIL, ADMIN_PASSWORD)

    response = await client.delete(
        f"/api/v1/users/{MEMBER_ID}",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 204

    response = await client.patch(
        PROTECTED_URL,
        json=PROTECTED_BODY,
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 401
    assert response.json()["code"] == "INVALID_CREDENTIALS"


@pytest.mark.xfail(
    reason="GET /api/v1/users is currently unauthenticated", strict=True
)
async def test_user_list_requires_authentication(client):
    response = await client.get("/api/v1/users")

    assert response.status_code == 401
