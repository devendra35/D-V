import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.api.chat import router as chat_router
from backend.api.profile import router as profile_router
from backend.api.projects import router as projects_router
from backend.api.skills import router as skills_router
from backend.config import settings
from backend.logging_config import configure_logging


configure_logging()

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application startup and shutdown."""

    logger.info(
        "Starting %s v%s in %s mode",
        settings.app_name,
        settings.app_version,
        settings.app_env,
    )

    yield

    logger.info(
        "Shutting down %s",
        settings.app_name,
    )


app = FastAPI(
    title=settings.app_name,
    description="The AI behind the developer.",
    version=settings.app_version,
    lifespan=lifespan,
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=[
        "GET",
        "POST",
        "PUT",
        "PATCH",
        "DELETE",
        "OPTIONS",
    ],
    allow_headers=["*"],
)


app.include_router(chat_router)
app.include_router(profile_router)
app.include_router(projects_router)
app.include_router(skills_router)


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
