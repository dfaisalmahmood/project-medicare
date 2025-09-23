from pydantic import BaseModel
import os


class Settings(BaseModel):
    app_name: str = "Project Medicare"
    debug: bool = os.getenv("DATABASE_DEBUG", "false").lower() == "true"

    # Database
    database_url: str = os.getenv(
        "DATABASE_URL",
        "postgresql+asyncpg://postgres:postgres@localhost:5451/project_medicare",
    )
    pool_size: int = int(os.getenv("DATABASE_POOL_SIZE", "5"))
    max_overflow: int = int(os.getenv("DATABASE_MAX_OVERFLOW", "10"))
    pool_recycle: int = int(os.getenv("DATABASE_POOL_RECYCLE", "3600"))  # seconds
    db_schema: str = os.getenv("DATABASE_SCHEMA", "public")

    # Security
    jwt_secret_key: str = os.getenv("JWT_SECRET_KEY", "change-me")
    jwt_algorithm: str = os.getenv("JWT_ALGORITHM", "HS256")
    access_token_expire_minutes: int = int(
        os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60")
    )

    # CORS
    cors_allow_origins: list[str] = (
        [o.strip() for o in os.getenv("CORS_ALLOW_ORIGINS", "*").split(",")]
        if os.getenv("CORS_ALLOW_ORIGINS")
        else ["*"]
    )
    cors_allow_credentials: bool = (
        os.getenv("CORS_ALLOW_CREDENTIALS", "true").lower() == "true"
    )
    cors_allow_methods: list[str] = (
        [m.strip() for m in os.getenv("CORS_ALLOW_METHODS", "*").split(",")]
        if os.getenv("CORS_ALLOW_METHODS")
        else ["*"]
    )
    cors_allow_headers: list[str] = (
        [h.strip() for h in os.getenv("CORS_ALLOW_HEADERS", "*").split(",")]
        if os.getenv("CORS_ALLOW_HEADERS")
        else ["*"]
    )


settings = Settings()
