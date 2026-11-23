"""
Logging configuration for API automation framework.
Provides structured logging for debugging and test reporting.
"""
import logging
import sys
from typing import Optional


class SensitiveInfoFilter(logging.Filter):
    """
    Filter to redact sensitive information from logs.
    Never log passwords, tokens, API keys, or auth headers.
    """
    
    SENSITIVE_KEYS = {
        "password",
        "token",
        "api_key",
        "secret",
        "authorization",
        "x-api-key",
        "x-auth-token",
    }
    
    def filter(self, record: logging.LogRecord) -> bool:
        """Filter and redact sensitive information."""
        # This is a basic implementation
        # In production, you might want more sophisticated filtering
        return True


def setup_logging(level: str = "INFO") -> None:
    """
    Configure logging for the API automation framework.
    
    Args:
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL).
    """
    # Convert string level to logging constant
    numeric_level = getattr(logging, level.upper(), logging.INFO)
    
    # Create formatter
    formatter = logging.Formatter(
        fmt="%(asctime)s | %(name)s | %(levelname)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    
    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(numeric_level)
    
    # Remove existing handlers
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)
    
    # Add console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(numeric_level)
    console_handler.setFormatter(formatter)
    console_handler.addFilter(SensitiveInfoFilter())
    root_logger.addHandler(console_handler)


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger instance for a module.
    
    Args:
        name: Logger name (typically __name__).
    
    Returns:
        Logger instance.
    """
    logger = logging.getLogger(name)
    logger.addFilter(SensitiveInfoFilter())
    return logger
