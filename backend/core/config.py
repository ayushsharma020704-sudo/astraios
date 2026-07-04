"""
ASTRAIOS Backend — Configuration
Loads settings from the root-level .env file (one directory above backend/).
"""

from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

# Resolve the root .env sitting one level above backend/
_ENV_FILE = Path(__file__).resolve().parents[2] / ".env"


class Settings(BaseSettings):
    """Central settings object — add new keys here as the project grows."""

    model_config = SettingsConfigDict(
        env_file=str(_ENV_FILE),
        env_file_encoding="utf-8",
        extra="ignore",  # silently skip keys we haven't declared yet
    )

    # --- App metadata ---
    APP_NAME: str = "ASTRAIOS"
    DEBUG: bool = False

    # --- API keys (all optional until the features that need them land) ---
    NASA_API_KEY: str = ""
    GROQ_API_KEY: str = ""
    GOOGLE_AI_STUDIO_KEY: str = ""
    HUGGINGFACE_TOKEN: str = ""
    NASA_ADS_TOKEN: str = ""

    # --- CORS ---
    CORS_ORIGINS: list[str] = ["http://localhost:5173"]


# Singleton — import `settings` wherever you need config values.
settings = Settings()
