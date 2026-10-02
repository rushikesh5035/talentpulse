from pydantic import BaseModel, EmailStr

# Schema for Login Request
class LoginRequest(BaseModel):
    email: EmailStr
    password: str

# Schema for Token Response
class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"  # Default value, no need to send from client

# Schema for Refresh Token Request
class RefreshTokenRequest(BaseModel):
    refresh_token: str

# Schema for Authenticated User Profile
class UserResponse(BaseModel):
    id: str
    email: EmailStr
    name: str
    role: str
    permissions: list[str] = []