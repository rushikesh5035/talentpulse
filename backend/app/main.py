from fastapi import FastAPI
from app.core.config import settings
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.router import api_router

# Initialize FastAPI APP
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="AI-Powered Recruitment & Candidate Matching API"
)

# CORS middleware configuration
app.add_middleware( 
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(
    api_router,
    prefix=settings.API_V1_STR
)

# Root Endpoints
@app.get("/", tags=["System"])
async def read_root():
    return {
        "message": f"Welcome to {settings.PROJECT_NAME} API 🚀",
        "docs": "/docs",
        "redoc": "/redoc",
        "version": settings.VERSION 
    }

# Health Check Endpoints
@app.get("/health", tags=["System"])
async def health_check():
    return {
        "status": "healthy",
        "service": settings.PROJECT_NAME,
        "debug_mode": settings.DEBUG
    }