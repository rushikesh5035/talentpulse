from fastapi import APIRouter

from app.schemas.question import QuestionEvaluateRequest, QuestionEvaluateResponse
from app.services.question_service import evaluate_answer

router = APIRouter(prefix="/questions", tags=["Questions"])


@router.post("/submit", response_model=QuestionEvaluateResponse)
async def submit_answer(request: QuestionEvaluateRequest) -> QuestionEvaluateResponse:
    evaluation = evaluate_answer(request)

    return QuestionEvaluateResponse(
        status="evaluated",
        evaluation=evaluation,
    )
