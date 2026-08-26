import os
from datetime import datetime, timedelta

from dotenv import load_dotenv
from jose import jwt
from passlib.context import CryptContext


load_dotenv()


SECRET_KEY = os.getenv("JWT_SECRET_KEY")

if not SECRET_KEY:
    raise RuntimeError(
        "JWT_SECRET_KEY environment variable is not configured."
    )


ALGORITHM = "HS256"
TOKEN_EXPIRE_HOURS = 8


pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
)


def hash_password(password: str) -> str:
    """Hash a user's password using bcrypt."""

    return pwd_context.hash(password)


def verify_password(
    password: str,
    hashed_password: str,
) -> bool:
    """Verify a plain-text password against its bcrypt hash."""

    return pwd_context.verify(
        password,
        hashed_password,
    )


def create_token(data: dict) -> str:
    """Create a signed JWT access token."""

    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(
        hours=TOKEN_EXPIRE_HOURS
    )

    to_encode.update(
        {
            "exp": expire,
        }
    )

    return jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM,
    )


def decode_token(token: str) -> dict:
    """Decode and validate a JWT access token."""

    return jwt.decode(
        token,
        SECRET_KEY,
        algorithms=[ALGORITHM],
    )
