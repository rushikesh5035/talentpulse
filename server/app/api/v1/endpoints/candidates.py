from fastapi import APIRouter, status

from app.schemas.candidate import (
    CandidateCreate,
    CandidateResponse,
    CandidateUploadRequest,
    CandidateUploadResponse,
)
from app.services.candidate_service import candidate_service

router = APIRouter(prefix="/candidates", tags=["Candidates"])


@router.post(
    "/add", response_model=CandidateResponse, status_code=status.HTTP_201_CREATED
)
async def add_candidate(candidate: CandidateCreate) -> CandidateResponse:
    return candidate_service.add(candidate)


@router.post(
    "/upload",
    response_model=CandidateUploadResponse,
    status_code=status.HTTP_201_CREATED,
)
async def upload_candidates(request: CandidateUploadRequest) -> CandidateUploadResponse:
    candidates = [candidate_service.add(candidate) for candidate in request.candidates]
    return CandidateUploadResponse(candidates=candidates, count=len(candidates))


@router.get("/", response_model=list[CandidateResponse])
async def list_candidates() -> list[CandidateResponse]:
    return candidate_service.list()
