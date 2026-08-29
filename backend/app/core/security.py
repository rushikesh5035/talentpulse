from datetime import datetime, timedelta, timezone
from typing import Any
import jwt
from pwdlib import PasswordHash
from app.core.config import settings

# Initialize modern password hashers    
password_hash = PasswordHash.recommended()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain password against its hash using pwdlib
    """
    try:
        return password_hash.verify(plain_password, hashed_password)
    except Exception:
        return False

def get_password_hash(password: str) -> str:
    """
    Hash a password securely using Argon2
    """
    return password_hash.hash(password)


def create_access_token(subject: str | Any, extra_claims: dict=None) -> str:
    """
    Generate a short-lived access JWT token (15 mins).
    """
    expire = datetime.now(timezone.utc) + timedelta(
        minutes= settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )

    to_encode = {
        "sub": str(subject),    # Subject (User Id/ email)
        "exp": expire,          # expiration
        "type" : "access"      # token type    
    }

    if extra_claims:
        to_encode.update(extra_claims)

    encoded_jwt = jwt.encode(
        to_encode,
        settings.JWT_ACCESS_SECRET,
        algorithm=settings.ALGORITHM
    )
    return encoded_jwt

def create_refresh_token(subject: str | Any) -> str:
    """
    Generate a long-lived refresh JWT token (30 days).
    """
    expire = datetime.now(timezone.utc) + timedelta(
        days= settings.REFRESH_TOKEN_EXPIRE_DAYS
    )

    to_encode = {
        "sub": str(subject),    # Subject (User Id/ email)
        "exp": expire,          # expiration
        "type" : "refresh"      # token type    
    }

    encoded_jwt = jwt.encode(
        to_encode,
        settings.JWT_REFRESH_SECRET,
        algorithm=settings.ALGORITHM
    )
    return encoded_jwt