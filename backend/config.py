from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application configuration."""

    # Application
    app_name: str = Field(default="DΞV")
    app_version: str = Field(default="0.1.0")
    app_env: str = Field(default="development")

    # Server
    host: str = Field(default="127.0.0.1")
    port: int = Field(default=8000, ge=1, le=65535)

    # CORS
    cors_origins: str = Field(
        default=(
            "http://localhost:5500,"
            "http://127.0.0.1:5500,"
            "http://localhost:3000"
        )
    )

    # Logging
    log_level: str = Field(default="INFO")

    # AI Providers
    groq_api_key: str = Field(default="")
    gemini_api_key: str = Field(default="")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    @property
    def cors_origin_list(self) -> list[str]:
        """Convert comma-separated CORS origins into a list."""

        return [
            origin.strip()
            for origin in self.cors_origins.split(",")
            if origin.strip()
        ]


@lru_cache
def get_settings() -> Settings:
    """Return a cached settings instance."""

    return Settings()


settings = get_settings()