import logging
from fastapi import FastAPI

from app.api.router import api_router
from app.core.config import settings
from app.core.db import Base, sessionmanager
import os
from app.modules.users import models as users_models  # ensure models are imported


def create_app() -> FastAPI:
    application = FastAPI(title=settings.app_name, debug=settings.debug)

    sessionmanager.init_db()
    # Create tables on startup only if explicitly enabled (avoid Alembic conflicts)
    if os.getenv("DB_AUTO_CREATE", "0") in {"1", "true", "True"}:
        try:
            Base.metadata.create_all(bind=sessionmanager.engine.sync_engine)
        except Exception as exc:
            logging.getLogger(__name__).warning(
                "Could not create database tables at startup: %s", exc
            )

    application.include_router(api_router, prefix="/api")

    @application.get("/")
    async def root():
        return {"message": "API ready", "app": settings.app_name}

    return application


app = create_app()
