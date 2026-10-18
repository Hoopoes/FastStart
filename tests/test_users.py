"""User CRUD tests, including the admin-only authorization rules."""

import pytest
from conftest import (
    ADMIN_EMAIL,
    ADMIN_ID,
    INACTIVE_EMAIL,
    INACTIVE_ID,
    MEMBER_EMAIL,
    MEMBER_ID,
    SECOND_ADMIN_ID,
)

USERS_URL = "/api/v1/users"


def user_url(user_id: int) -> str:
    return f"{USERS_URL}/{user_id}"


# ---------------------------------------------------------------------------
# Read
# ---------------------------------------------------------------------------


async def test_list_users(client):
    response = await client.get(USERS_URL)

    assert response.status_code == 200
    body = response.json()
    assert len(body["users"]) == 3
    assert body["page"] == 1
    assert body["limit"] == 20
    assert body["total"] == 3
    assert body["pages"] == 1


async def test_list_users_pagination_metadata(client):
    first = (await client.get(USERS_URL, params={"page": 1, "limit": 2})).json()
    second = (await client.get(USERS_URL, params={"page": 2, "limit": 2})).json()

    assert [user["id"] for user in first["users"]] == [1, 2]
    assert first["page"] == 1
    assert first["limit"] == 2
    assert first["total"] == 3
    assert first["pages"] == 2

    assert [user["id"] for user in second["users"]] == [3]
    assert second["page"] == 2
    assert second["total"] == 3


async def test_list_users_page_beyond_last_is_empty(client):
    body = (await client.get(USERS_URL, params={"page": 5, "limit": 2})).json()

    assert body["users"] == []
    assert body["total"] == 3


async def test_list_users_never_exposes_password_hashes(client):
    response = await client.get(USERS_URL)

    for user in response.json()["users"]:
        assert "hashed_password" not in user
        assert "password" not in user


@pytest.mark.parametrize(
    ("params", "expected_emails"),
    [
        ({"role": "admin"}, [ADMIN_EMAIL]),
        ({"role": "member"}, [MEMBER_EMAIL, INACTIVE_EMAIL]),
        ({"active": "false"}, [INACTIVE_EMAIL]),
        ({"active": "true"}, [ADMIN_EMAIL, MEMBER_EMAIL]),
    ],
)
async def test_list_users_filters(client, params, expected_emails):
    response = await client.get(USERS_URL, params=params)

    assert response.status_code == 200
    body = response.json()
    assert [user["email"] for user in body["users"]] == expected_emails
    assert body["total"] == len(expected_emails)


async def test_list_users_search_matches_name_and_email(client):
    by_name = await client.get(USERS_URL, params={"search": "mubba"})
    by_email = await client.get(USERS_URL, params={"search": "inactive@"})

    assert len(by_name.json()["users"]) == 1
    assert len(by_email.json()["users"]) == 1


async def test_get_user(client):
    response = await client.get(user_url(ADMIN_ID))

    assert response.status_code == 200
    assert response.json()["email"] == ADMIN_EMAIL


async def test_get_unknown_user(client):
    response = await client.get(user_url(9999))

    assert response.status_code == 404
    assert response.json()["code"] == "USER_NOT_FOUND"


# ---------------------------------------------------------------------------
# Create
# ---------------------------------------------------------------------------


async def test_create_user_then_authenticate(client):
    response = await client.post(
        USERS_URL,
        json={
            "name": "New User",
            "email": "new@example.com",
            "password": "secret123",
            "role": "member",
        },
    )

    assert response.status_code == 201
    assert response.json()["code"] == "SUCCESS"

    login_response = await client.post(
        "/api/token", data={"username": "new@example.com", "password": "secret123"}
    )
    assert login_response.status_code == 200, "created user should be able to log in"


async def test_create_user_defaults_to_member_role(client):
    await client.post(
        USERS_URL,
        json={
            "name": "No Role",
            "email": "norole@example.com",
            "password": "secret123",
        },
    )

    response = await client.get(USERS_URL, params={"search": "norole@"})

    assert response.json()["users"][0]["role"] == "member"


@pytest.mark.parametrize("email", [ADMIN_EMAIL, ADMIN_EMAIL.upper()])
async def test_create_user_duplicate_email_conflicts(client, email):
    response = await client.post(
        USERS_URL,
        json={"name": "Duplicate", "email": email, "password": "secret123"},
    )

    assert response.status_code == 409
    # NOTE: the code name is misleading, the conflict is on email, not id.
    assert response.json()["code"] == "USER_ALREADY_EXISTS"


async def test_create_user_rejects_special_characters_in_name(client):
    response = await client.post(
        USERS_URL,
        json={
            "name": "Bad!Name",
            "email": "bad@example.com",
            "password": "secret123",
        },
    )

    assert response.status_code == 400
    assert response.json()["code"] == "USER_NAME_INVALID"


# ---------------------------------------------------------------------------
# Replace (PUT) - admin only
# ---------------------------------------------------------------------------


async def test_replace_requires_admin(client, member_headers):
    response = await client.put(
        user_url(INACTIVE_ID),
        json={
            "name": "Ayesha Ali",
            "email": INACTIVE_EMAIL,
            "role": "member",
            "active": True,
        },
        headers=member_headers,
    )

    assert response.status_code == 403
    assert response.json()["code"] == "ADMIN_REQUIRED"


async def test_admin_replaces_member(client, admin_headers):
    response = await client.put(
        user_url(INACTIVE_ID),
        json={
            "name": "Ayesha Ali",
            "email": INACTIVE_EMAIL,
            "role": "member",
            "active": True,
        },
        headers=admin_headers,
    )

    assert response.status_code == 200
    assert response.json()["active"] is True


async def test_admin_cannot_replace_self(client, admin_headers):
    response = await client.put(
        user_url(ADMIN_ID),
        json={
            "name": "Umar Ahmed",
            "email": ADMIN_EMAIL,
            "role": "admin",
            "active": True,
        },
        headers=admin_headers,
    )

    assert response.status_code == 403
    assert response.json()["code"] == "CANNOT_REPLACE_SELF"


async def test_admin_cannot_replace_other_admin(client, admin_headers, second_admin):
    response = await client.put(
        user_url(SECOND_ADMIN_ID),
        json={
            "name": "Renamed Admin",
            "email": "second@example.com",
            "role": "admin",
            "active": True,
        },
        headers=admin_headers,
    )

    assert response.status_code == 403
    assert response.json()["code"] == "CANNOT_REPLACE_ADMIN"


async def test_replace_unknown_user(client, admin_headers):
    response = await client.put(
        user_url(9999),
        json={
            "name": "Ghost User",
            "email": "ghost@example.com",
            "role": "member",
            "active": True,
        },
        headers=admin_headers,
    )

    assert response.status_code == 404
    assert response.json()["code"] == "USER_NOT_FOUND"


async def test_replace_conflicting_email(client, admin_headers):
    response = await client.put(
        user_url(INACTIVE_ID),
        json={
            "name": "Ayesha Ali",
            "email": ADMIN_EMAIL,
            "role": "member",
            "active": True,
        },
        headers=admin_headers,
    )

    assert response.status_code == 409
    assert response.json()["code"] == "USER_ALREADY_EXISTS"


# ---------------------------------------------------------------------------
# Update (PATCH) - authenticated only
# ---------------------------------------------------------------------------


async def test_patch_requires_authentication(client):
    response = await client.patch(user_url(MEMBER_ID), json={"active": False})

    assert response.status_code == 401


async def test_admin_patches_member(client, admin_headers):
    response = await client.patch(
        user_url(MEMBER_ID), json={"active": False}, headers=admin_headers
    )

    assert response.status_code == 200
    assert response.json()["active"] is False


async def test_patch_rejects_empty_body(client, admin_headers):
    response = await client.patch(user_url(MEMBER_ID), json={}, headers=admin_headers)

    assert response.status_code == 422


async def test_patch_unknown_user(client, admin_headers):
    response = await client.patch(
        user_url(9999), json={"active": False}, headers=admin_headers
    )

    assert response.status_code == 404
    assert response.json()["code"] == "USER_NOT_FOUND"


async def test_patch_does_not_accept_email(client, admin_headers):
    """UpdateUserDto has no email field, so PATCH cannot change the address.

    FastAPI drops the unknown field, which leaves UpdateUserDto empty and trips
    the `at_least_one_field` validator. Only the message is 422-worthy; the
    status is a side effect of the unknown field being ignored.
    """
    response = await client.patch(
        user_url(INACTIVE_ID), json={"email": MEMBER_EMAIL}, headers=admin_headers
    )

    assert response.status_code == 422
    assert response.json()["code"] == "REQ_VALIDATION_FAILED"


async def test_patch_changes_role(client, admin_headers):
    response = await client.patch(
        user_url(MEMBER_ID), json={"role": "admin"}, headers=admin_headers
    )

    assert response.status_code == 200
    assert response.json()["role"] == "admin"


async def test_member_can_patch_any_user(client, member_headers):
    """Documents current behaviour: PATCH is authenticated-only, not admin-only."""
    response = await client.patch(
        user_url(INACTIVE_ID), json={"active": True}, headers=member_headers
    )

    assert response.status_code == 200


# ---------------------------------------------------------------------------
# Delete - admin only
# ---------------------------------------------------------------------------


async def test_delete_requires_authentication(client):
    response = await client.delete(user_url(MEMBER_ID))

    assert response.status_code == 401


async def test_delete_requires_admin(client, member_headers):
    response = await client.delete(user_url(MEMBER_ID), headers=member_headers)

    assert response.status_code == 403
    assert response.json()["code"] == "ADMIN_REQUIRED"


async def test_admin_deletes_member(client, admin_headers):
    response = await client.delete(user_url(MEMBER_ID), headers=admin_headers)

    assert response.status_code == 204
    assert (await client.get(user_url(MEMBER_ID))).status_code == 404


async def test_admin_cannot_delete_self(client, admin_headers):
    response = await client.delete(user_url(ADMIN_ID), headers=admin_headers)

    assert response.status_code == 403
    assert response.json()["code"] == "CANNOT_DELETE_SELF"


async def test_admin_cannot_delete_other_admin(client, admin_headers, second_admin):
    response = await client.delete(user_url(SECOND_ADMIN_ID), headers=admin_headers)

    assert response.status_code == 403
    assert response.json()["code"] == "CANNOT_DELETE_ADMIN"


# ---------------------------------------------------------------------------
# Known gaps, kept as xfail so they flip to a failure once fixed
# ---------------------------------------------------------------------------


@pytest.mark.xfail(
    reason="POST /api/v1/users is unauthenticated and accepts role=admin", strict=True
)
async def test_create_user_requires_authentication(client):
    response = await client.post(
        USERS_URL,
        json={
            "name": "Escalated Admin",
            "email": "escalated@example.com",
            "password": "secret123",
            "role": "admin",
        },
    )

    assert response.status_code == 401


@pytest.mark.xfail(
    reason="PATCH is authenticated-only, any member can edit any user", strict=True
)
async def test_patch_requires_admin(client, member_headers):
    response = await client.patch(
        user_url(ADMIN_ID),
        json={"active": False},
        headers=member_headers,
    )

    assert response.status_code == 403


@pytest.mark.xfail(
    reason="PATCH is authenticated-only and role is patchable, so any member "
    "can promote themselves to admin",
    strict=True,
)
async def test_member_cannot_promote_themselves(client, member_headers):
    response = await client.patch(
        user_url(MEMBER_ID), json={"role": "admin"}, headers=member_headers
    )

    assert response.status_code == 403
