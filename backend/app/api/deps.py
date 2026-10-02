from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import jwt
from app.core.config import settings
from app.schemas.auth import UserResponse


# this tells fastapi where the login endpoint is
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/auth/login")

async def get_current_user(token: str = Depends(oauth2_scheme)) -> UserResponse:
    """
    Decode and validate the JWT access token.
    Returns the current authenticated user's data.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        # Decode the JWT
        payload = jwt.decode(
            token,
            settings.JWT_ACCESS_SECRET,
            algorithms=[settings.ALGORITHM],
        )

        # Extract subject (email)
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception

        # Ensure it's an access token, not a refresh token
        if payload.get("type") != "access":
            raise credentials_exception
    
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Access token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.InvalidTokenError:
        raise credentials_exception

    return UserResponse(
        id=payload.get("sub"),
        email=email,
        name=payload.get("name", ""),
        role=payload.get("role", "candidate"),
        permissions=payload.get("permissions", []),
    )

def require_role(*roles: str):
    """
    Factory that returns a dependency requiring one of the specified rules.
    Usage: Depends(require_role("admin", "recruiter"))
    """
    async def role_checker(current_user: UserResponse = Depends(get_current_user)):
        if current_user.role not in roles:
            raise HTTPException(
                detail=f"Access denied. Required roles: {list(roles)}",
            )
        
        return current_user
    return role_checker