from app.auth.models import User
from app.auth.hashing_service import hash_password, verify_password


fake_users_db = {
    "admin": {
        "username": "admin",
        "full_name": "John Doe",
        "email": "admin@example.com",
        "hashed_password": hash_password(password="admin123"),
    }
}


def authenticate_user(username: str, password: str):
    if username in fake_users_db:
        if verify_password(password, fake_users_db[username]["hashed_password"]):
            return User(username=username)
    return None


def get_user(username: str):
    if username in fake_users_db:
        return User(username=username)
    return None
