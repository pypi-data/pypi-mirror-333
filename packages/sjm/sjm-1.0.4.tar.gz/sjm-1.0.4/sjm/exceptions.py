"""
SJM AI Client - Exceptions

This module defines the exception classes used by the SJM client.
All exceptions inherit from the base SJMError class.
"""

from typing import Optional, Dict, Any


class SJMError(Exception):
    """Base exception class for all SJM API errors."""

    def __init__(self, message: str, http_status: Optional[int] = None, response: Optional[Dict[str, Any]] = None):
        """
        Initialize a new SJM error.

        Args:
            message: Error message
            http_status: Optional HTTP status code
            response: Optional API response data
        """
        self.message = message
        self.http_status = http_status
        self.response = response
        super().__init__(self.message)


class SJMAuthenticationError(SJMError):
    """
    Raised when authentication fails.
    
    This typically occurs when:
    - An invalid API key is provided
    - The API key has been revoked
    - The API key doesn't have permission to access the requested resource
    """
    
    def __init__(self, message: str, http_status: Optional[int] = None, response: Optional[Dict[str, Any]] = None):
        """
        Initialize a new authentication error.

        Args:
            message: Error message
            http_status: Optional HTTP status code (typically 401)
            response: Optional API response data
        """
        super().__init__(message, http_status, response)


class SJMAPIError(SJMError):
    """
    Raised when the SJM API returns an error.
    
    This indicates a problem with the request or on the server side.
    The error message will include details about what went wrong.
    """
    
    def __init__(self, message: str, http_status: Optional[int] = None, response: Optional[Dict[str, Any]] = None, 
                 error_code: Optional[str] = None):
        """
        Initialize a new API error.

        Args:
            message: Error message
            http_status: Optional HTTP status code
            response: Optional API response data
            error_code: Optional error code from the API
        """
        self.error_code = error_code
        super().__init__(message, http_status, response)


class SJMRateLimitError(SJMError):
    """
    Raised when the SJM API rate limit is exceeded.
    
    This occurs when too many requests are made in a short period.
    The client should implement exponential backoff or wait before retrying.
    """
    
    def __init__(self, message: str, http_status: Optional[int] = None, 
                 response: Optional[Dict[str, Any]] = None, reset_at: Optional[int] = None,
                 limit: Optional[int] = None, remaining: Optional[int] = None):
        """
        Initialize a new rate limit error.

        Args:
            message: Error message
            http_status: Optional HTTP status code (typically 429)
            response: Optional API response data
            reset_at: Optional timestamp when the rate limit will reset
            limit: Optional rate limit maximum
            remaining: Optional remaining requests allowed
        """
        self.reset_at = reset_at
        self.limit = limit
        self.remaining = remaining
        super().__init__(message, http_status, response)


class SJMTimeoutError(SJMError):
    """
    Raised when a request to the SJM API times out.
    
    This can occur due to network issues or if the API operation
    takes longer than the specified timeout period.
    """
    
    def __init__(self, message: str, timeout: Optional[float] = None):
        """
        Initialize a new timeout error.

        Args:
            message: Error message
            timeout: The timeout duration in seconds
        """
        self.timeout = timeout
        super().__init__(message)


class SJMValidationError(SJMError):
    """
    Raised when input validation fails.
    
    This occurs when the client provides invalid parameters to an API method.
    The error message will include details about which parameters are invalid.
    """
    
    def __init__(self, message: str, field_errors: Optional[Dict[str, str]] = None, 
                 http_status: Optional[int] = None, response: Optional[Dict[str, Any]] = None):
        """
        Initialize a new validation error.

        Args:
            message: Error message
            field_errors: Dictionary mapping field names to error messages
            http_status: Optional HTTP status code (typically 400)
            response: Optional API response data
        """
        self.field_errors = field_errors or {}
        super().__init__(message, http_status, response)


class SJMResourceNotFoundError(SJMError):
    """
    Raised when a requested resource doesn't exist.
    
    This can occur when trying to access a freelancer, project,
    or other resource that does not exist in the system.
    """
    
    def __init__(self, message: str, resource_type: Optional[str] = None, 
                 resource_id: Optional[str] = None, http_status: Optional[int] = None, 
                 response: Optional[Dict[str, Any]] = None):
        """
        Initialize a new resource not found error.

        Args:
            message: Error message
            resource_type: Type of resource that wasn't found (e.g., "freelancer")
            resource_id: ID of the resource that wasn't found
            http_status: Optional HTTP status code (typically 404)
            response: Optional API response data
        """
        self.resource_type = resource_type
        self.resource_id = resource_id
        super().__init__(message, http_status, response)


class SJMInsufficientPermissionsError(SJMAuthenticationError):
    """
    Raised when the API key doesn't have sufficient permissions.
    
    This occurs when the API key is valid but doesn't have the
    required permissions to perform the requested operation.
    """
    
    def __init__(self, message: str, required_permission: Optional[str] = None, 
                 http_status: Optional[int] = None, response: Optional[Dict[str, Any]] = None):
        """
        Initialize a new insufficient permissions error.

        Args:
            message: Error message
            required_permission: The permission that was required
            http_status: Optional HTTP status code (typically 403)
            response: Optional API response data
        """
        self.required_permission = required_permission
        super().__init__(message, http_status, response)


class SJMServerError(SJMError):
    """
    Raised when the SJM API experiences an internal server error.
    
    This indicates a problem on the server side. These errors should be 
    reported to the SJM team for investigation.
    """
    
    def __init__(self, message: str, http_status: Optional[int] = None, 
                 response: Optional[Dict[str, Any]] = None, request_id: Optional[str] = None):
        """
        Initialize a new server error.

        Args:
            message: Error message
            http_status: Optional HTTP status code (typically 5xx)
            response: Optional API response data
            request_id: Optional request ID for troubleshooting with the SJM team
        """
        self.request_id = request_id
        super().__init__(message, http_status, response)
