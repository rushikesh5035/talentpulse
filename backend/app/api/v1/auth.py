from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
import jwt

from app.schemas.auth import TokenResponse, RefreshTokenRequest, UserResponse
from app.core.security import (
    verify_password,
    create_access_token,
    create_refresh_token,
)
from app.core.config import settings
from app.core.database import get_db
from app.api.deps import get_current_user
from app.services.user_service import get_user_by_email

router = APIRouter()

# Permission mapping by role (until we build a proper permissions table)
ROLE_PERMISSIONS = {
    "admin" : ["create:job", "edit:job", "view:analytics", "configure:ai", "view:candidates"],
    "recruiter": ["create:job", "edit:job", "view:candidates"],
    "hiring_manager": ["view:candidates", "view:analytics"],
    "candidate": [],
}

# ── POST /api/v1/auth/login
@router.post("/login", response_model=TokenResponse)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db)
):
    """
    Authenticate a user and return access + refresh tokens.
    Accepts oauth2 form data (username=email, password)
    """

    email = form_data.username     
    password = form_data.password

    # 1. Query database for the email
    user = await get_user_by_email(db, email)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    # 2. verify password against hashed password
    if not verify_password(password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    # 3. check if account is active
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account inactive. Please contact support",
        )

    # 4. Create tokens
    permissions = ROLE_PERMISSIONS.get(user.role, [])
    extra_claims = {
        "role": user.role,
        "permissions": permissions,
        "name": user.name,
    }

    # generate access and refresh token
    access_token = create_access_token(subject=user.email, extra_claims=extra_claims)
    refresh_token = create_refresh_token(subject=user.email)

    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
    )

# ── POST /api/v1/auth/refresh 
@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(
    request: RefreshTokenRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Issue a new access token using a valid refresh toekn
    """

    try:
        payload = jwt.decode(
            request.refresh_token,
            settings.JWT_REFRESH_SECRET,
            algorithm=[settings.ALGORITHM],
        )

        # ensure this is actually a refresh token
        if payload.get("type") != refresh:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token type", 
            )
        
        email = payload.get('sub')
        user = await get_user_by_email(db, email)
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found",
            )

        permissions = ROLE_PERMISSIONS.get(user.role, [])
        extra_claims = {
            "role": user.role,
            "permissions": permissions,
            "name": user.name
        }

        new_access_token = create_access_token(subject=email, extra_claims=extra_claims)
        new_refresh_token = create_refresh_token(subject=email)

        return TokenResponse(
            access_token = new_access_token,
            refresh_token = new_refresh_token
        )

    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token has expired. Please log in again"
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
        )

# ── GET /api/v1/auth/me 
@router.get("/me", response_model=UserResponse)
async def get_me(current_user: UserResponse = Depends(get_current_user)):
    """
    Returns the currently authenticated user's profile.
    Requires a valid Bearer access token
    """
    return current_user
