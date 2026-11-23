from pydantic_settings import BaseSettings
from typing import List, Optional


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

    # Email Configuration
    mail_enabled: bool = False  # Set to True when email is configured
    mail_from: str = "noreply@portfolio.com"
    mail_from_name: str = "Portfolio Contact Form"
    mail_to: Optional[str] = None  # Your email address to receive contact form messages
    
    # SMTP Settings
    smtp_host: Optional[str] = None  # e.g., "smtp.gmail.com"
    smtp_port: int = 587
    smtp_username: Optional[str] = None
    smtp_password: Optional[str] = None
    smtp_tls: bool = True
    smtp_ssl: bool = False

    @property
    def cors_origins_list(self) -> List[str]:
        return [origin.strip() for origin in self.cors_origins.split(",")]

    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
