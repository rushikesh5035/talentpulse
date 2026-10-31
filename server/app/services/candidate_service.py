from uuid import uuid4

from app.schemas.candidate import CandidateCreate, CandidateResponse

class CandidateService:
    """Temporary process-local candidate store for development."""

    def __init__(self) -> None:
        self._candidates: dict[str, CandidateResponse] = {}

    def add(self, candidate: CandidateCreate) -> CandidateResponse:
        candidate_id = f"candidate_{uuid4().hex}"

        result = CandidateResponse(
            id=candidate_id,
            name=candidate.name,
            email=candidate.email,
            experience=candidate.experience,
            skills=candidate.skills,
            status="processed",
        )

        self._candidates[candidate_id] = result
        return result

    def list(self) -> list[CandidateResponse]:
        return list(self._candidates.values())


candidate_service = CandidateService()