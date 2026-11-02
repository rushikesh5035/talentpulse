from pydantic import BaseModel, EmailStr


class UserResponse(BaseModel):
    id: str
    name: str
    email: EmailStr
    role: str
    permissions: list[str]


class TokenPayload(BaseModel):
    sub: str
    user_id: str
    name: str
    role: str
    permissions: list[str]
