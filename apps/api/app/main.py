"""FastAPI application factory; feature routes are added in later milestones."""

from fastapi import FastAPI

from app.settings import Settings, get_settings


def create_app(settings: Settings | None = None) -> FastAPI:
    """Build the API application with explicit, injectable configuration."""

    resolved_settings = settings or get_settings()
    application = FastAPI(
        title=resolved_settings.app_name,
        version="0.1.0",
        docs_url=None if resolved_settings.app_env == "production" else "/docs",
        redoc_url=None if resolved_settings.app_env == "production" else "/redoc",
    )
    application.state.settings = resolved_settings
    return application


app = create_app()
