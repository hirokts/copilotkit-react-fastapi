from functools import cached_property

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    cors_origins: str = "http://localhost:5173"
    openai_api_key: str = ""
    jwt_secret: str = "dev-secret-key"
    database_url: str = "postgresql://postgres:postgres@localhost:5432/app"

    @cached_property
    def cors_origins_list(self) -> list[str]:
        return [origin.strip() for origin in self.cors_origins.split(",")]


settings = Settings()
