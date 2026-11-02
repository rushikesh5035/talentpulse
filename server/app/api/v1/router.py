from fastapi import APIRouter

from app.api.v1.endpoints import candidates, evaluations, health, jobs, questions

api_router = APIRouter()

api_router.include_router(health.router)
api_router.include_router(jobs.router)
api_router.include_router(candidates.router)
api_router.include_router(questions.router)
api_router.include_router(evaluations.router)
