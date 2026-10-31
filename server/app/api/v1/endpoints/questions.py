from fastapi import APIRouter

from app.schemas.question import (
    QuestionGenerateRequest,
    QuestionGenerateResponse
)
from app.services.question_service import generate_questions

router = APIRouter(prefix="/questions", tags=["Questions"])


@router.post("/generate", response_model=QuestionGenerateResponse)
async def generate_interview_questions(request: QuestionGenerateRequest) -> QuestionGenerateResponse:
    questions = generate_questions(request)

    return QuestionGenerateResponse(
        questions=questions,
        count=len(questions),
        source="template"
    )