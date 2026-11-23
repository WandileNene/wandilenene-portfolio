"""
Base API client for all API interactions.
Provides common functionality for HTTP requests, error handling, and logging.
"""
import json
from typing import Any, Dict, Optional
import requests
from requests import Response
import allure

from api_automation.config import get_config
from api_automation.utils import get_logger


logger = get_logger(__name__)


class APIResponse:
    """Wrapper around requests.Response for easier assertions."""
    
    def __init__(self, response: Response):
        """Initialize with a requests Response object."""
        self._response = response
    
    @property
    def status_code(self) -> int:
        """Get HTTP status code."""
        return self._response.status_code
    
    @property
    def headers(self) -> Dict[str, str]:
        """Get response headers."""
        return dict(self._response.headers)
    
    def json(self) -> Any:
        """Parse response JSON."""
        return self._response.json()
    
    @property
    def text(self) -> str:
        """Get response text."""
        return self._response.text
    
    @property
    def content(self) -> bytes:
        """Get response content (bytes)."""
        return self._response.content
    
    def is_success(self) -> bool:
        """Check if response is successful (2xx status code)."""
        return 200 <= self.status_code < 300
    
    def is_error(self) -> bool:
        """Check if response is an error (4xx or 5xx status code)."""
        return self.status_code >= 400
    
    def __repr__(self) -> str:
        return f"APIResponse(status={self.status_code})"


class BaseAPIClient:
    """
    Base API client providing common HTTP functionality.
    
    Handles:
    - Base URL management
    - Headers and authentication
    - Request/response logging
    - Error handling
    - Timeouts
    """
    
    def __init__(self, base_url: Optional[str] = None, timeout: Optional[int] = None):
        """
        Initialize API client.
        
        Args:
            base_url: Override base URL from config.
            timeout: Override timeout from config.
        """
        config = get_config()
        self.base_url = base_url or config.base_url
        self.timeout = timeout or config.timeout
        self.session = requests.Session()
        self.logger = get_logger(self.__class__.__name__)
    
    def _log_request(self, method: str, url: str, **kwargs) -> None:
        """Log request details for debugging."""
        self.logger.debug(f"{method} {url}")
        if "json" in kwargs:
            self.logger.debug(f"Payload: {json.dumps(kwargs['json'], indent=2)}")
        if "params" in kwargs:
            self.logger.debug(f"Query params: {kwargs['params']}")
    
    def _log_response(self, response: Response) -> None:
        """Log response details for debugging."""
        self.logger.debug(f"Status: {response.status_code}")
        try:
            self.logger.debug(f"Response: {json.dumps(response.json(), indent=2)}")
        except (json.JSONDecodeError, ValueError):
            self.logger.debug(f"Response (text): {response.text[:500]}")
    
    def _attach_to_allure(self, method: str, url: str, response: Response, **kwargs) -> None:
        """Attach request/response details to Allure report."""
        # Attach request
        request_info = f"{method} {url}"
        if "json" in kwargs:
            request_info += f"\n\nBody:\n{json.dumps(kwargs['json'], indent=2)}"
        if "params" in kwargs:
            request_info += f"\n\nQuery Params:\n{json.dumps(kwargs['params'], indent=2)}"
        
        allure.attach(request_info, "Request", allure.attachment_type.TEXT)
        
        # Attach response
        response_info = f"Status: {response.status_code}\n\nHeaders:\n{json.dumps(dict(response.headers), indent=2)}"
        try:
            response_info += f"\n\nBody:\n{json.dumps(response.json(), indent=2)}"
        except (json.JSONDecodeError, ValueError):
            response_info += f"\n\nBody:\n{response.text}"
        
        allure.attach(response_info, "Response", allure.attachment_type.TEXT)
    
    def get(
        self,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        **kwargs
    ) -> APIResponse:
        """
        Perform a GET request.
        
        Args:
            endpoint: API endpoint (without base URL).
            params: Query parameters.
            **kwargs: Additional arguments to pass to requests.
        
        Returns:
            APIResponse wrapper.
        """
        url = f"{self.base_url}{endpoint}"
        kwargs.setdefault("timeout", self.timeout)
        if params:
            kwargs["params"] = params
        
        self._log_request("GET", url, **kwargs)
        response = self.session.get(url, **kwargs)
        self._log_response(response)
        self._attach_to_allure("GET", url, response, **kwargs)
        
        return APIResponse(response)
    
    def post(
        self,
        endpoint: str,
        json: Optional[Dict[str, Any]] = None,
        data: Optional[Any] = None,
        **kwargs
    ) -> APIResponse:
        """
        Perform a POST request.
        
        Args:
            endpoint: API endpoint.
            json: JSON payload.
            data: Form data or other data.
            **kwargs: Additional arguments.
        
        Returns:
            APIResponse wrapper.
        """
        url = f"{self.base_url}{endpoint}"
        kwargs.setdefault("timeout", self.timeout)
        
        if json is not None:
            kwargs["json"] = json
        if data is not None:
            kwargs["data"] = data
        
        self._log_request("POST", url, **kwargs)
        response = self.session.post(url, **kwargs)
        self._log_response(response)
        self._attach_to_allure("POST", url, response, **kwargs)
        
        return APIResponse(response)
    
    def patch(
        self,
        endpoint: str,
        json: Optional[Dict[str, Any]] = None,
        **kwargs
    ) -> APIResponse:
        """
        Perform a PATCH request.
        
        Args:
            endpoint: API endpoint.
            json: JSON payload.
            **kwargs: Additional arguments.
        
        Returns:
            APIResponse wrapper.
        """
        url = f"{self.base_url}{endpoint}"
        kwargs.setdefault("timeout", self.timeout)
        
        if json is not None:
            kwargs["json"] = json
        
        self._log_request("PATCH", url, **kwargs)
        response = self.session.patch(url, **kwargs)
        self._log_response(response)
        self._attach_to_allure("PATCH", url, response, **kwargs)
        
        return APIResponse(response)
    
    def put(
        self,
        endpoint: str,
        json: Optional[Dict[str, Any]] = None,
        **kwargs
    ) -> APIResponse:
        """
        Perform a PUT request.
        
        Args:
            endpoint: API endpoint.
            json: JSON payload.
            **kwargs: Additional arguments.
        
        Returns:
            APIResponse wrapper.
        """
        url = f"{self.base_url}{endpoint}"
        kwargs.setdefault("timeout", self.timeout)
        
        if json is not None:
            kwargs["json"] = json
        
        self._log_request("PUT", url, **kwargs)
        response = self.session.put(url, **kwargs)
        self._log_response(response)
        self._attach_to_allure("PUT", url, response, **kwargs)
        
        return APIResponse(response)
    
    def delete(
        self,
        endpoint: str,
        **kwargs
    ) -> APIResponse:
        """
        Perform a DELETE request.
        
        Args:
            endpoint: API endpoint.
            **kwargs: Additional arguments.
        
        Returns:
            APIResponse wrapper.
        """
        url = f"{self.base_url}{endpoint}"
        kwargs.setdefault("timeout", self.timeout)
        
        self._log_request("DELETE", url, **kwargs)
        response = self.session.delete(url, **kwargs)
        self._log_response(response)
        self._attach_to_allure("DELETE", url, response, **kwargs)
        
        return APIResponse(response)
    
    def close(self) -> None:
        """Close the session."""
        self.session.close()
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()
