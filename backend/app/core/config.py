from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # App metadata
    PROJECT_NAME: str = "TalentPulse AI"
    VERSION: str = "1.0.0"
    DEBUG: bool = True
    API_V1_STR: str = "/api/v1"

    # CORS Origins
    BACKEND_CORS_ORIGINS: list[str] = [
        "http://localhost:5173",
        "http://localhost:3000" 
    ]

    # JWT Security
    JWT_ACCESS_SECRET: str
    JWT_REFRESH_SECRET: str
    ALGORITHM: str = "HS256"

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 30

    # Environment configuration
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True
    )

# Instantiate a single global settings object
settings = Settings()