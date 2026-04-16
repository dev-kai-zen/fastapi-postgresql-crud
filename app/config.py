from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

_BASE_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=_BASE_DIR / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )
    database_url: str  # from env DATABASE_URL
    redis_url: str  # from env REDIS_URL

    # If not database_url
    # database_url: str = Field(validation_alias="CUSTOM_DATABASE_URL")
    # redis_url: str = Field(validation_alias="CUSTOM_REDIS_URL")


# Env / .env supply fields; pyright cannot see that at call time.
settings = Settings()  # type: ignore[call-arg]
