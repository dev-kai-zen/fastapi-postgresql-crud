from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

_BASE_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=_BASE_DIR / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_name: str  # from env APP_NAME
    environment: str = "development"

    api_v1_prefix: str = "/api/v1"

    database_url: str  # from env DATABASE_URL
    redis_url: str  # from env REDIS_URL

    jwt_secret_key: str  # from env JWT_SECRET_KEY
    jwt_algorithm: str  # from env JWT_ALGORITHM
    access_token_expire_minutes: int  # from env ACCESS_TOKEN_EXPIRE_MINUTES
    refresh_token_expire_days: int  # from env REFRESH_TOKEN_EXPIRE_DAYS


# Env / .env supply fields; pyright cannot see that at call time.
def get_settings() -> Settings:
    return Settings()  # type: ignore[call-arg]
