from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    # Application
    app_name: str = "Portfolio API"
    app_version: str = "1.0.0"
    debug: bool = True
    environment: str = "development"

    # Server
    host: str = "0.0.0.0"
    port: int = 8000

    # CORS
    cors_origins: str = "http://localhost:3000,http://localhost:5173"

    # Database
    database_url: str = "sqlite:///./portfolio.db"

    # Security
    secret_key: str = "portfolio-dev-secret-key"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    @property
    def cors_origins_list(self) -> List[str]:
        return [origin.strip() for origin in self.cors_origins.split(",")]

    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
