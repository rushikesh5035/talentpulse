from datetime import datetime, timedelta, timezone

import jwt

from app.core.config import get_settings
from app.schemas.user import TokenPayload, UserResponse


def create_access_token(user: UserResponse) -> tuple[str, int]:
    settings = get_settings()
    expires_in = settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
    expires_at = datetime.now(timezone.utc) + timedelta(seconds=expires_in)

    payload = {
        "sub": user.email,
        "user_id": user.id,
        "name": user.name,
        "role": user.role,
        "permissions": user.permissions,
        "exp": expires_at,
    }

    token = jwt.encode(
        payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM
    )

    return token, expires_in


def decode_access_token(token: str) -> TokenPayload:
    settings = get_settings()
    payload = jwt.decode(
        token,
        settings.JWT_SECRET_KEY,
        algorithms=[settings.JWT_ALGORITHM],
        options={"require": ["sub", "exp"]},
    )

    return TokenPayload(
        sub=payload["sub"],
        user_id=payload["user_id"],
        name=payload["name"],
        role=payload["role"],
        permissions=payload["permissions"],
    )
