"""
SJM AI Client - Official Python client for the SJM AI API

This package provides a convenient interface to the SJM AI API,
allowing developers to easily integrate with SJM's freelancer matching,
skill verification, and AI-powered interview capabilities.

Basic usage:
    from sjm import SJM

    # Initialize client with your API key
    client = SJM(api_key="your_api_key")

    # Match freelancers to a project
    matches = client.match(
        description="Build a modern web application with React",
        required_skills=["React.js", "Node.js", "TypeScript"]
    )

    # Print top matches
    for match in matches["matches"][:3]:
        freelancer = match["freelancer"]
        print(f"{freelancer['name']} - Score: {match['score']:.2f}")
"""

# Version information
__title__ = "sjm"
__description__ = "Official Python client for the SJM AI API"
__url__ = "https://snapjobsai.com"
__version__ = "1.0.0"
__author__ = "SJM AI Team"
__author_email__ = "support@snapjobsai.com"
__license__ = "MIT"

# Import key components for easier access
from .client import SJM
from .exceptions import (
    SJMError,
    SJMAuthenticationError,
    SJMAPIError, 
    SJMRateLimitError,
    SJMTimeoutError,
    SJMValidationError,
    SJMResourceNotFoundError,
    SJMInsufficientPermissionsError,
    SJMServerError
)
from .models import Freelancer, Match, HealthStatus

# Define what gets imported with "from sjm import *"
__all__ = [
    "SJM",
    "SJMError", 
    "SJMAuthenticationError", 
    "SJMAPIError",
    "SJMRateLimitError",
    "SJMTimeoutError",
    "SJMValidationError",
    "SJMResourceNotFoundError", 
    "SJMInsufficientPermissionsError",
    "SJMServerError",
    "Freelancer", 
    "Match", 
    "HealthStatus"
]
