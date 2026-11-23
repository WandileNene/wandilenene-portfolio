"""
Configuration module for API automation framework.
Manages environment-specific settings and credentials.
"""
import os
from dataclasses import dataclass
from typing import Optional


@dataclass
class Config:
    """Configuration settings for API automation."""
    
    base_url: str
    environment: str
    debug: bool
    timeout: int = 30
    log_level: str = "INFO"
    
    # Allure settings
    allure_dir: str = "allure-results"
    
    @classmethod
    def from_env(cls, env: Optional[str] = None) -> "Config":
        """
        Load configuration from environment variables.
        
        Args:
            env: Environment name (dev, qa, staging). Defaults to 'dev'.
        
        Returns:
            Config instance with settings from environment.
        """
        environment = env or os.getenv("API_ENV", "dev").lower()
        
        # Environment-specific base URLs
        base_urls = {
            "dev": os.getenv("DEV_BASE_URL", "http://localhost:8000"),
            "qa": os.getenv("QA_BASE_URL", "http://qa-api.example.com"),
            "staging": os.getenv("STAGING_BASE_URL", "http://staging-api.example.com"),
        }
        
        return cls(
            base_url=base_urls.get(environment, base_urls["dev"]),
            environment=environment,
            debug=os.getenv("DEBUG", "false").lower() == "true",
            timeout=int(os.getenv("API_TIMEOUT", "30")),
            log_level=os.getenv("LOG_LEVEL", "INFO"),
            allure_dir=os.getenv("ALLURE_DIR", "allure-results"),
        )
    
    def __str__(self) -> str:
        return (
            f"Config(env={self.environment}, "
            f"base_url={self.base_url}, "
            f"debug={self.debug}, "
            f"timeout={self.timeout}s)"
        )


# Global config instance
_config: Optional[Config] = None


def get_config(env: Optional[str] = None) -> Config:
    """
    Get or create the global configuration instance.
    
    Args:
        env: Optional environment name override.
    
    Returns:
        Global Config instance.
    """
    global _config
    if _config is None:
        _config = Config.from_env(env)
    return _config


def set_config(config: Config) -> None:
    """
    Set the global configuration instance (useful for testing).
    
    Args:
        config: Config instance to set.
    """
    global _config
    _config = config
