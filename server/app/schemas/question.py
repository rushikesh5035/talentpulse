from pydantic import BaseModel, Field

class QuestionGenerateRequest(BaseModel):
    job_description: str = Field(min_length=1, max_length=50_000)
    job_skills: list[str] = Field(default_factory=list, max_length=100)
    candidate_skills: list[str] = Field(default_factory=list, max_length=100)

class QuestionGenerateResponse(BaseModel):
    questions: list[str]
    count: int = Field(ge=0)
    source: str
