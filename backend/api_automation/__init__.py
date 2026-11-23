"""
API Automation Framework
Comprehensive API testing framework with Pytest and Allure reporting.
"""

__version__ = "1.0.0"
__author__ = "QA Team"

from api_automation.config import Config, get_config, set_config
from api_automation.clients import BaseAPIClient, APIResponse
from api_automation.utils import get_logger, setup_logging

__all__ = [
    "Config",
    "get_config",
    "set_config",
    "BaseAPIClient",
    "APIResponse",
    "get_logger",
    "setup_logging",
]
