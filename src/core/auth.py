import jwt
import os

from datetime import datetime, timedelta, timezone
from hashlib import blake2b
from hmac import compare_digest


def make_password(password: str) -> str:
    """Hash a password.

    Parameters:
        password (str): The password to hash.

    Returns:
        str: The hashed password.
    """
    return blake2b(password.encode()).hexdigest()


def verify_password(password: str, hashed_password: str) -> bool:
    """Verify a password.

    Parameters:
        password (str): The password to verify.
        hashed_password (str): The hashed password.

    Returns:
        bool: True if the password is correct, False otherwise.
    """
    h = make_password(password)
    return compare_digest(h, hashed_password)


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """Create a new access token.

    Parameters:
        data (dict): The data to include in the token.
        expires_delta (timedelta | None): The expiration time for the token.

    Returns:
        str: The access token.
    """
    data_to_encode = data.copy()
    expire: datetime

    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=10)

    data_to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        data_to_encode,
        os.environ.get("SECRET_KEY"),
        algorithm=os.environ.get("HASH_ALGORITHM"),
    )

    return encoded_jwt
