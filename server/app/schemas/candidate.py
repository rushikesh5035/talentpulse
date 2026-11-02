from pydantic import BaseModel, EmailStr, Field


class CandidateCreate(BaseModel):
    name: str = Field(min_length=1, max_length=150)
    email: EmailStr
    resume: str = Field(min_length=1, max_length=50_000)
    experience: str | None = Field(default=None, max_length=500)
    skills: list[str] = Field(default_factory=list, max_length=100)


class CandidateResponse(BaseModel):
    id: str
    name: str
    email: EmailStr
    experience: str | None
    skills: list[str]
    status: str


class CandidateUploadRequest(BaseModel):
    candidates: list[CandidateCreate] = Field(min_length=1, max_length=50)


class CandidateUploadResponse(BaseModel):
    candidates: list[CandidateResponse]
    count: int
