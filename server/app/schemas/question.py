from pydantic import BaseModel, Field


class QuestionGenerateRequest(BaseModel):
    job_description: str = Field(min_length=1, max_length=50_000)
    job_skills: list[str] = Field(default_factory=list, max_length=100)
    candidate_skills: list[str] = Field(default_factory=list, max_length=100)


class QuestionGenerateResponse(BaseModel):
    questions: list[str]
    count: int = Field(ge=0)
    source: str


class QuestionEvaluateRequest(BaseModel):
    question: str = Field(min_length=1, max_length=5_000)
    answer: str = Field(min_length=1, max_length=20_000)
    context: str = Field(default="", max_length=50_000)


class QuestionEvaluation(BaseModel):
    score: int = Field(ge=1, le=10)
    feedback: str
    improvements: str


class QuestionEvaluateResponse(BaseModel):
    status: str
    evaluation: QuestionEvaluation