from fastapi import APIRouter

from app.core.config import get_settings

# creating an instance of APIRouter
router = APIRouter(tags=["Health"])

@router.get("/health")
async def health_check() -> dict:
    """
    Health check endpoint to verify that the API is running.
    """
    settings = get_settings()
    return {
        "status": "healthy", 
        "message": "API is running smoothly.", 
        "version": settings.VERSION,
    }
