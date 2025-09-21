from pydantic import BaseModel
import os


class Settings(BaseModel):
    app_name: str = "Project Medicare"
    debug: bool = os.getenv("DEBUG", "false").lower() == "true"

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


settings = Settings()
