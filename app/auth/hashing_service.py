import os
import base64
import hashlib


def hash_token(token: str) -> str:
    return hashlib.sha256(token.encode()).hexdigest()

# -----------------------------
# Secure Password Hashing
# -----------------------------
def hash_password(password: str) -> str:
    """
    Hash a password securely with PBKDF2-HMAC-SHA256 and a random 16-byte salt.
    Returns base64(salt + hash)
    """
    salt = os.urandom(16)
    pwd_hash = hashlib.pbkdf2_hmac(
        "sha256",  # Hash function
        password.encode("utf-8"),  # Convert password to bytes
        salt,
        200_000,  # Number of iterations, high enough for security
    )
    # Store as base64: salt + hash
    return base64.b64encode(salt + pwd_hash).decode("utf-8")


def verify_password(password: str, stored_hash: str) -> bool:
    """
    Verify a password against the stored hash.
    """
    decoded = base64.b64decode(stored_hash.encode("utf-8"))
    salt = decoded[:16]
    original_hash = decoded[16:]
    test_hash = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 200_000)
    return test_hash == original_hash


if __name__ == "__main__":
    hashed_pw = hash_password(password="admin123")
    print(verify_password(password="admin123", stored_hash=hashed_pw))