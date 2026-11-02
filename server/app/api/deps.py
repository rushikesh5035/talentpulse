from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.core.config import get_settings
from app.core.security import decode_access_token
from app.schemas.user import TokenPayload, UserResponse


bearer_scheme = HTTPBearer(
    scheme_name="BearerAuth",
    bearerFormat="JWT",
    description="Paste the access token returned by POST /api/v1/auth/login.",
)

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


# def get_current_user(
#     token: Annotated[str, Depends(oauth2_scheme)],
# ) -> UserResponse:
#     try:
#         claims: TokenPayload = decode_access_token(token)
#     except (jwt.InvalidTokenError, KeyError, ValueError):
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Invalid or expired access token",
#             headers={"WWW-Authenticate": "Bearer"},
#         )

#     return UserResponse(
#         id=claims.user_id,
#         email=claims.sub,
#         name=claims.name,
#         role=claims.role,
#         permissions=claims.permissions,
#     )


# CurrentUser = Annotated[UserResponse, Depends(get_current_user)]


def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(bearer_scheme)],
) -> UserResponse:
    token = credentials.credentials
    try:
        claims: TokenPayload = decode_access_token(token)
    except jwt.InvalidTokenError, KeyError, ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired access token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return UserResponse(
        id=claims.user_id,
        email=claims.sub,
        name=claims.name,
        role=claims.role,
        permissions=claims.permissions,
    )


CurrentUser = Annotated[UserResponse, Depends(get_current_user)]
