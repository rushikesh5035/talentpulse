from pydantic import BaseModel, Field


class JobAnalysisRequest(BaseModel):
    job_description: str = Field(
        min_length=1, description="The full job description to analyze."
    )


class JobAnalysisResponse(BaseModel):
    title: str
    skills: list[str]
    summary: str
    scoreHint: int = Field(ge=0, le=100)
    job_id: str
    storage_status: str
    matching_candidates: list[dict[str, object]]
    candidate_count: int = Field(ge=0)
