"""
Tests for the SJM client library.

This module contains tests for the SJM client using pytest.
It uses mocking to simulate API responses and test error handling.
"""

import pytest
import requests
import json
import os
from unittest.mock import patch, MagicMock, mock_open

from sjm.client import SJM
from sjm.exceptions import (
    SJMError,
    SJMAuthenticationError,
    SJMAPIError,
    SJMRateLimitError,
    SJMTimeoutError,
    SJMValidationError,
    SJMResourceNotFoundError,
    SJMServerError
)

# Test constants
API_KEY = "sjm_test_key"
BASE_URL = "https://test-api.sjm.com/api/v1/docker"

# Fixtures
@pytest.fixture
def client():
    """Create a test client instance."""
    return SJM(api_key=API_KEY, base_url=BASE_URL)

@pytest.fixture
def mock_response():
    """Create a mock response object."""
    response = MagicMock()
    response.status_code = 200
    response.headers = {}
    response.json.return_value = {"status": "success"}
    return response

@pytest.fixture
def mock_session():
    """Create a patched session for the client."""
    with patch("requests.Session") as mock:
        session_instance = MagicMock()
        session_instance.headers = {}
        session_instance.request.return_value = MagicMock(
            status_code=200,
            json=lambda: {"status": "success"},
            headers={}
        )
        mock.return_value = session_instance
        yield mock

# Test basic client functionality
def test_client_init():
    """Test client initialization."""
    client = SJM(api_key=API_KEY, base_url=BASE_URL)
    assert client.api_key == API_KEY
    assert client.base_url == BASE_URL

def test_client_init_trailing_slash():
    """Test client initialization with trailing slash in base URL."""
    client = SJM(api_key=API_KEY, base_url=BASE_URL + "/")
    assert client.base_url == BASE_URL  # Should strip trailing slash

# Test request method
def test_request(client, mock_session):
    """Test the _request method with a GET request."""
    result = client._request("GET", "/health")
    
    # Verify the session was called correctly
    client.session.request.assert_called_once_with(
        method="GET",
        url=f"{BASE_URL}/health",
        params=None,
        json=None,
        timeout=30
    )
    
    # Verify the result
    assert result == {"status": "success"}

def test_request_with_params(client, mock_session):
    """Test the _request method with parameters."""
    params = {"limit": 10}
    client._request("GET", "/test", params=params)
    
    client.session.request.assert_called_once_with(
        method="GET",
        url=f"{BASE_URL}/test",
        params=params,
        json=None,
        timeout=30
    )

def test_request_with_data(client, mock_session):
    """Test the _request method with a JSON body."""
    data = {"name": "Test"}
    client._request("POST", "/test", data=data)
    
    client.session.request.assert_called_once_with(
        method="POST",
        url=f"{BASE_URL}/test",
        params=None,
        json=data,
        timeout=30
    )

def test_request_with_files(client, mock_session):
    """Test the _request method with file uploads."""
    files = {"file": ("test.pdf", "file content")}
    headers = {"X-API-Key": API_KEY}
    
    # Set up the session mock to handle the headers.copy() call
    client.session.headers = headers.copy()
    
    client._request("POST", "/upload", files=files)
    
    # Verify that Content-Type was removed for file uploads
    client.session.request.assert_called_once()
    call_args = client.session.request.call_args[1]
    assert call_args["files"] == files
    assert "Content-Type" not in call_args["headers"]

# Test error handling
def test_auth_error(client, mock_session):
    """Test authentication error handling."""
    # Set up the mock to return a 401 error
    response = MagicMock()
    response.status_code = 401
    response.text = "Unauthorized"
    client.session.request.return_value = response
    
    with pytest.raises(SJMAuthenticationError) as excinfo:
        client._request("GET", "/test")
    
    assert "authentication failed" in str(excinfo.value).lower()

def test_rate_limit_error(client, mock_session):
    """Test rate limit error handling."""
    # Set up the mock to return a 429 error
    response = MagicMock()
    response.status_code = 429
    response.text = "Rate limit exceeded"
    client.session.request.return_value = response
    
    with pytest.raises(SJMRateLimitError) as excinfo:
        client._request("GET", "/test")
    
    assert "rate limit exceeded" in str(excinfo.value).lower()

def test_api_error(client, mock_session):
    """Test general API error handling."""
    # Set up the mock to return a 400 error with JSON response
    response = MagicMock()
    response.status_code = 400
    response.json.return_value = {"detail": "Bad request"}
    response.text = '{"detail": "Bad request"}'
    client.session.request.return_value = response
    
    with pytest.raises(SJMAPIError) as excinfo:
        client._request("GET", "/test")
    
    assert "400" in str(excinfo.value)
    assert "bad request" in str(excinfo.value).lower()

def test_api_error_with_text(client, mock_session):
    """Test API error with text response."""
    # Set up the mock to return a 500 error with text response
    response = MagicMock()
    response.status_code = 500
    response.json.side_effect = ValueError("Invalid JSON")
    response.text = "Internal Server Error"
    client.session.request.return_value = response
    
    with pytest.raises(SJMAPIError) as excinfo:
        client._request("GET", "/test")
    
    assert "500" in str(excinfo.value)
    assert "internal server error" in str(excinfo.value).lower()

def test_request_exception(client):
    """Test handling of request exceptions."""
    # Simulate a connection error
    with patch("requests.Session.request") as mock_request:
        mock_request.side_effect = requests.exceptions.ConnectionError("Connection failed")
        
        with pytest.raises(SJMAPIError) as excinfo:
            client._request("GET", "/test")
        
        assert "request failed" in str(excinfo.value).lower()
        assert "connection failed" in str(excinfo.value).lower()

# Test API methods
def test_health(client, mock_session):
    """Test the health method."""
    client.session.request.return_value.json.return_value = {
        "status": "healthy",
        "components": {
            "data_source": {"status": "healthy"},
            "skill_extractor": {"status": "ready"}
        }
    }
    
    result = client.health()
    
    client.session.request.assert_called_once_with(
        method="GET",
        url=f"{BASE_URL}/health",
        params=None,
        json=None,
        timeout=30
    )
    
    assert result["status"] == "healthy"
    assert "components" in result
    assert result["components"]["data_source"]["status"] == "healthy"

def test_match(client, mock_session):
    """Test the match method."""
    # Sample response data
    matches_response = {
        "status": "success",
        "matches": [
            {
                "freelancer": {
                    "id": "f1",
                    "name": "John Doe",
                    "job_title": "Web Developer",
                    "skills": ["React.js", "Node.js"],
                    "experience": 5,
                    "rating": 4.8,
                    "hourly_rate": 50.0,
                    "availability": True,
                    "total_sales": 100
                },
                "score": 0.95,
                "matching_skills": 2
            }
        ]
    }
    client.session.request.return_value.json.return_value = matches_response
    
    # Call the match method
    result = client.match(
        description="Test project",
        required_skills=["React.js", "Node.js"],
        budget_range=(1000, 5000),
        complexity="medium",
        timeline=30
    )
    
    # Verify the request
    client.session.request.assert_called_once()
    call_args = client.session.request.call_args[1]
    assert call_args["method"] == "POST"
    assert call_args["url"] == f"{BASE_URL}/match"
    
    # Verify the request data
    request_data = call_args["json"]
    assert request_data["description"] == "Test project"
    assert request_data["required_skills"] == ["React.js", "Node.js"]
    assert request_data["budget_range"] == (1000, 5000)
    assert request_data["complexity"] == "medium"
    assert request_data["timeline"] == 30
    
    # Verify the result
    assert result == matches_response
    assert result["status"] == "success"
    assert len(result["matches"]) == 1
    assert result["matches"][0]["freelancer"]["name"] == "John Doe"
    assert result["matches"][0]["score"] == 0.95

def test_verify_skill(client, mock_session):
    """Test the verify_skill method."""
    # Sample response
    skill_response = {
        "status": "success",
        "data": {
            "exists": True,
            "skills": ["React.js"],
            "similar_terms": []
        }
    }
    client.session.request.return_value.json.return_value = skill_response
    
    # Call the verify_skill method
    result = client.verify_skill("React.js")
    
    # Verify the request
    client.session.request.assert_called_once()
    call_args = client.session.request.call_args[1]
    assert call_args["method"] == "POST"
    assert call_args["url"] == f"{BASE_URL}/verify-skill"
    
    # Verify the request data
    request_data = call_args["json"]
    assert request_data["keyword"] == "React.js"
    
    # Verify the result
    assert result == skill_response
    assert result["data"]["exists"] == True
    assert "React.js" in result["data"]["skills"]

def test_interview(client, mock_session):
    """Test the interview method."""
    # Sample response
    interview_response = {
        "status": "success",
        "data": {
            "freelancer": {
                "id": "f1",
                "name": "John Doe",
                "job_title": "Web Developer"
            },
            "mode": "ai_questions",
            "session_id": "session123",
            "interview_data": {
                "questions": [
                    {
                        "text": "Tell me about your React.js experience.",
                        "scoring_criteria": {"technical": 40, "experience": 30, "communication": 30}
                    }
                ]
            }
        }
    }
    client.session.request.return_value.json.return_value = interview_response
    
    # Call the interview method
    result = client.interview(
        freelancer_id="f1",
        project_description="Test project",
        required_skills=["React.js", "Node.js"],
        job_title="Web Developer",
        mode="ai_questions"
    )
    
    # Verify the request
    client.session.request.assert_called_once()
    call_args = client.session.request.call_args[1]
    assert call_args["method"] == "POST"
    assert call_args["url"] == f"{BASE_URL}/interview"
    
    # Verify the request data
    request_data = call_args["json"]
    assert request_data["freelancer_id"] == "f1"
    assert request_data["project_description"] == "Test project"
    assert request_data["required_skills"] == ["React.js", "Node.js"]
    assert request_data["job_title"] == "Web Developer"
    assert request_data["mode"] == "ai_questions"
    
    # Verify the result
    assert result == interview_response
    assert result["data"]["session_id"] == "session123"
    assert len(result["data"]["interview_data"]["questions"]) == 1

def test_interview_with_session_and_answers(client, mock_session):
    """Test the interview method with session ID and answers."""
    # Sample response
    interview_response = {
        "status": "success",
        "data": {
            "freelancer": {
                "id": "f1",
                "name": "John Doe",
                "job_title": "Web Developer"
            },
            "mode": "ai_full",
            "session_id": "session123",
            "evaluation": {
                "overall_score": 85,
                "strengths": ["Good technical knowledge"]
            }
        }
    }
    client.session.request.return_value.json.return_value = interview_response
    
    # Call the interview method with session and answers
    result = client.interview(
        freelancer_id="f1",
        project_description="Test project",
        required_skills=["React.js", "Node.js"],
        job_title="Web Developer",
        mode="ai_full",
        session_id="session123",
        provided_answers=["I have 5 years of React experience"]
    )
    
    # Verify the request
    client.session.request.assert_called_once()
    call_args = client.session.request.call_args[1]
    
    # Verify the request data
    request_data = call_args["json"]
    assert request_data["session_id"] == "session123"
    assert request_data["provided_answers"] == ["I have 5 years of React experience"]
    
    # Verify the result
    assert result == interview_response
    assert "evaluation" in result["data"]
    assert result["data"]["evaluation"]["overall_score"] == 85

def test_generate_test_data(client, mock_session):
    """Test the generate_test_data method."""
    # Sample response
    test_data_response = {
        "status": "success",
        "data": [
            {
                "id": "f1",
                "name": "Test User 1",
                "job_title": "Web Developer",
                "skills": ["React.js", "Node.js"],
                "experience": 5,
                "rating": 4.8,
                "hourly_rate": 50.0,
                "availability": True,
                "total_sales": 100
            }
        ]
    }
    client.session.request.return_value.json.return_value = test_data_response
    
    # Call the generate_test_data method
    result = client.generate_test_data(num_freelancers=10)
    
    # Verify the request
    client.session.request.assert_called_once()
    call_args = client.session.request.call_args[1]
    assert call_args["method"] == "GET"
    assert call_args["url"] == f"{BASE_URL}/generate-test-data?num_freelancers=10"
    
    # Verify the result
    assert result == test_data_response
    assert len(result["data"]) == 1
    assert result["data"][0]["name"] == "Test User 1"

def test_parse_resume(client, mock_session):
    """Test the parse_resume method."""
    # Sample response
    parse_response = {
        "status": "success",
        "data": {
            "skills": ["React.js", "Node.js"],
            "experience": [],
            "education": [],
            "contact": {
                "email": None,
                "phone": None,
                "location": None
            }
        }
    }
    client.session.request.return_value.json.return_value = parse_response
    
    # Mock the open function
    mock_file = mock_open(read_data=b"test file content")
    
    # Call the parse_resume method with the mocked open
    with patch("builtins.open", mock_file):
        result = client.parse_resume("resume.pdf")
    
    # Verify the request
    client.session.request.assert_called_once()
    call_args = client.session.request.call_args[1]
    assert call_args["method"] == "POST"
    assert call_args["url"] == f"{BASE_URL}/parse"
    assert "files" in call_args
    assert call_args["files"]["file"][0] == "resume.pdf"
    
    # Verify the result
    assert result == parse_response
    assert "skills" in result["data"]
    assert "React.js" in result["data"]["skills"]

# Run the tests using pytest
if __name__ == "__main__":
    pytest.main(["-v"])
