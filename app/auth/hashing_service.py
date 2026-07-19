from pwdlib import PasswordHash

# -----------------------------
# Secure Password Hashing
# -----------------------------

password_hasher = PasswordHash.recommended()


def hash_password(password: str) -> str:
    return password_hasher.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    """
    Verify a password against the stored hash.
    """
    return password_hasher.verify(password, hashed_password)


if __name__ == "__main__":
    hashed_pw = hash_password(password="admin123")
    print(verify_password(password="admin123", hashed_password=hashed_pw))
