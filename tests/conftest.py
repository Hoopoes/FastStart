# ruff: noqa: E402
"""Shared fixtures for the FastStart test suite.

`CONFIG` is built at import time from the environment, so the required keys are
filled in below *before* anything imports `config`. `load_dotenv()` does not
override already-set variables, so these values win over `.env`.
"""

import pytest
import pytest_asyncio
from dotenv import load_dotenv
from httpx import ASGITransport, AsyncClient

from app.auth.hashing_service import hash_password
from app.server import app
from app.services.dummy_data import USERS

load_dotenv()

# Demo credentials from app/services/dummy_data.py
ADMIN_EMAIL = "admin@example.com"
ADMIN_PASSWORD = "admin123"
ADMIN_ID = 1

MEMBER_EMAIL = "member@example.com"
MEMBER_PASSWORD = "member123"
MEMBER_ID = 2

INACTIVE_EMAIL = "inactive@example.com"
INACTIVE_PASSWORD = "member1234"
INACTIVE_ID = 3

SECOND_ADMIN_EMAIL = "second@example.com"
SECOND_ADMIN_PASSWORD = "second123"
SECOND_ADMIN_ID = 99


@pytest.fixture(autouse=True)
def isolate_user_store():
    """Undo every mutation the in-memory store receives during a test."""
    snapshot = [dict(user) for user in USERS]
    yield
    USERS[:] = snapshot


@pytest_asyncio.fixture
async def client():
    """Async HTTP client talking to the ASGI app in-process."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as c:
        yield c


async def login(client: AsyncClient, email: str, password: str) -> str:
    """Authenticate and return the raw access token."""
    response = await client.post(
        "/api/token",
        data={"username": email, "password": password},
    )
    assert response.status_code == 200, response.text
    return response.json()["access_token"]


async def auth_headers(client: AsyncClient, email: str, password: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {await login(client, email, password)}"}


@pytest_asyncio.fixture
async def admin_headers(client) -> dict[str, str]:
    return await auth_headers(client, ADMIN_EMAIL, ADMIN_PASSWORD)


@pytest_asyncio.fixture
async def member_headers(client) -> dict[str, str]:
    return await auth_headers(client, MEMBER_EMAIL, MEMBER_PASSWORD)


@pytest.fixture
def second_admin() -> dict:
    """Append another admin so the 'other admin' rules can be exercised."""
    user = {
        "id": SECOND_ADMIN_ID,
        "name": "Second Admin",
        "email": SECOND_ADMIN_EMAIL,
        "hashed_password": hash_password(SECOND_ADMIN_PASSWORD),
        "role": "admin",
        "active": True,
    }
    USERS.append(user)
    return user
