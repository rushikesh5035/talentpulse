from uuid import uuid4

from fastapi import APIRouter

from app.schemas.job import JobAnalysisRequest, JobAnalysisResponse
from app.services.job_service import parse_job_description

router = APIRouter(prefix="/jobs", tags=["jobs"])


@router.post("/analyze", response_model=JobAnalysisResponse)
async def analyze_job(request: JobAnalysisRequest) -> JobAnalysisResponse:
    parsed = parse_job_description(request.job_description)

    return JobAnalysisResponse(
        **parsed,
        job_id=f"job_{uuid4().hex}",
        storage_status="partial",
        matching_candidates=[],
        candidate_count=0,
    )
