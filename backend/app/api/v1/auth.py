from fastapi import APIRouter, HTTPException, status, Depends
from app.schemas.auth import LoginRequest, TokenResponse, RefreshTokenRequest, UserResponse
from app.core.security import (
    verify_password,
    get_password_hash,
    create_access_token,
    create_refresh_token,
)
import jwt
from app.core.config import settings
from app.api.deps import get_current_user
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter()

# Mock user database
MOCK_USERS = {
    "admin@talentpulse.com": {
        "id": "1",
        "name": "Admin User",
        "role": "admin",
        "permissions": ["create:job", "edit:job", "view:analytics", "configure:ai"],
        # password: "admin123"
        "hashed_password": get_password_hash("admin123"),
    },
    "recruiter@talentpulse.com": {
        "id": "2",
        "name": "Recruiter User",
        "role": "recruiter",
        "permissions": ["create:job", "edit:job", "view:candidates"],
        # password: "recruiter123"
        "hashed_password": get_password_hash("recruiter123"),
    },
}

# ── POST /api/v1/auth/login
@router.post("/login", response_model=TokenResponse)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Authenticate a user and return access + refresh tokens.
    Accepts oauth2 form data (username=email, password)
    """

    email = form_data.username     
    password = form_data.password

    # check if user exists
    user = MOCK_USERS.get(email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    # verify password
    if not verify_password(password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )
    
    # create tokens with extra claims (role, permissions)
    extra_claims = {
        "role": user["role"],
        "permissions": user["permissions"],
        "name": user["name"],
    }

    # generate access and refresh token
    access_token = create_access_token(subject=email, extra_claims=extra_claims)
    refresh_token = create_refresh_token(subject=email)

    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
    )

# ── POST /api/v1/auth/refresh 
@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(request: RefreshTokenRequest):
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
        user = MOCK_USERS.get(email)
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found",
            )
        
        extra_claims = {
            "role": user["role"],
            "permissions": user["permissions"],
            "name": user["name"]
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

@router.get("/me", response_model=UserResponse)
async def get_me(current_user: UserResponse = Depends(get_current_user)):
    """
    Returns the currently authenticated user's profile.
    Requires a valid Bearer access token
    """
    return current_user
