from app.auth.hashing_service import hash_password

USERS = [
    {
        "id": 1,
        "name": "Umar Ahmed",
        "email": "admin@example.com",
        "hashed_password": hash_password(password="admin123"),
        "role": "admin",
        "active": True,
    },
    {
        "id": 2,
        "name": "Mubbashir Khan",
        "email": "member@example.com",
        "hashed_password": hash_password(password="member123"),
        "role": "member",
        "active": True,
    },
    {
        "id": 3,
        "name": "Ayesha Ali",
        "email": "inactive@example.com",
        "hashed_password": hash_password(password="member1234"),
        "role": "member",
        "active": False,
    },
]