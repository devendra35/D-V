import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.api.chat import router as chat_router
from backend.config import settings
from backend.logging_config import configure_logging


# Configure application logging
configure_logging()

logger = logging.getLogger(__name__)


# Create FastAPI application
app = FastAPI(
    title=settings.app_name,
    description="The AI behind the developer.",
    version=settings.app_version,
)


# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)


# Register API routers
app.include_router(chat_router)


@app.get("/", tags=["System"])
async def root() -> dict[str, str]:
    """Return basic DΞV application information."""

    return {
        "name": "DΞV",
        "message": "The AI behind the developer.",
        "status": "online",
    }


@app.get("/health", tags=["System"])
async def health() -> dict[str, str]:
    """Return the application health status."""

    return {
        "name": "DΞV",
        "status": "online",
    }


@app.on_event("startup")
async def startup_event() -> None:
    """Run startup tasks."""

    logger.info(
        "Starting %s v%s in %s mode",
        settings.app_name,
        settings.app_version,
        settings.app_env,
    )


@app.on_event("shutdown")
async def shutdown_event() -> None:
    """Run shutdown tasks."""

    logger.info("Shutting down %s", settings.app_name)