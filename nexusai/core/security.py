"""
Security Utilities for NexusAI OS.
JWT Authentication and Password Hashing via bcrypt.
"""
from datetime import datetime, timedelta, timezone
from typing import Optional
import bcrypt
from jwt import encode as jwt_encode, decode as jwt_decode, PyJWTError

from nexusai.core.config import settings


def hash_password(password: str) -> str:
    """Hashes plain text password using bcrypt."""
    pwd_bytes = password.encode('utf-8')[:72]
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(pwd_bytes, salt).decode('utf-8')


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifies plain text password against hash."""
    pwd_bytes = plain_password.encode('utf-8')[:72]
    hash_bytes = hashed_password.encode('utf-8')
    return bcrypt.checkpw(pwd_bytes, hash_bytes)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Encodes JWT access token with expiration timestamp."""
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt_encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def decode_access_token(token: str) -> Optional[dict]:
    """Decodes and validates JWT token."""
    try:
        payload = jwt_decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except PyJWTError:
        return None
