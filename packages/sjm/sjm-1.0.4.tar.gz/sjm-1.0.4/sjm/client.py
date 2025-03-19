"""
SJM AI Client - Main API client implementation

This module provides the main SJM client class for interacting with
the SJM AI API for freelancer matching, interviews, and skill verification.
"""

import requests
import json
import os
import pkg_resources
from typing import Dict, List, Optional, Union, Any, Tuple, BinaryIO
from .exceptions import SJMAuthenticationError, SJMAPIError, SJMRateLimitError

# Get version from package metadata
try:
    __version__ = pkg_resources.get_distribution("sjm").version
except pkg_resources.DistributionNotFound:
    __version__ = "1.0.0"  # Default version if not installed as package

class SJM:
    """
    Client for the SJM AI API
    
    This client provides convenient access to the SJM AI API
    for matching freelancers, conducting interviews, and verifying skills.
    """
    def __init__(
        self, 
        api_key: str, 
        base_url: str = "https://snapjobsai.com/api/v1/docker"
    ):
        """
        Initialize the SJM client.
        
        Args:
            api_key: Your SJM API key
            base_url: The base URL for the SJM API
        """
        self.api_key = api_key
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        self.session.headers.update({
            "X-API-Key": self.api_key,
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": f"sjm-python-client/{__version__}"
        })
    
    def _request(
        self, 
        method: str, 
        endpoint: str, 
        params: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
        files: Optional[Dict[str, Any]] = None,
        timeout: int = 30
    ) -> Dict[str, Any]:
        """
        Make a request to the SJM API.
        
        Args:
            method: HTTP method
            endpoint: API endpoint
            params: Query parameters
            data: Request body
            files: Files to upload
            timeout: Request timeout in seconds
            
        Returns:
            API response as a dictionary
            
        Raises:
            SJMAuthenticationError: If authentication fails
            SJMRateLimitError: If rate limit is exceeded
            SJMAPIError: For other API errors
        """
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        
        try:
            if files:
                # For file uploads, don't use JSON
                headers = self.session.headers.copy()
                headers.pop("Content-Type", None)
                response = self.session.request(
                    method=method,
                    url=url,
                    params=params,
                    data=data,
                    files=files,
                    headers=headers,
                    timeout=timeout
                )
            else:
                # Standard JSON request
                response = self.session.request(
                    method=method,
                    url=url,
                    params=params,
                    json=data,
                    timeout=timeout
                )
            
            # Store rate limit information
            self.rate_limit_limit = response.headers.get("X-RateLimit-Limit")
            self.rate_limit_remaining = response.headers.get("X-RateLimit-Remaining")
            self.rate_limit_reset = response.headers.get("X-RateLimit-Reset")
            
            # Check for API errors
            if response.status_code == 401:
                raise SJMAuthenticationError("Invalid API key or authentication failed")
            elif response.status_code == 429:
                raise SJMRateLimitError("API rate limit exceeded")
            elif response.status_code >= 400:
                error_message = f"API error: {response.status_code}"
                try:
                    error_data = response.json()
                    if "detail" in error_data:
                        error_message = f"{error_message} - {error_data['detail']}"
                    elif "error" in error_data:
                        error_message = f"{error_message} - {error_data['error']}"
                except Exception:
                    error_message = f"{error_message} - {response.text}"
                raise SJMAPIError(error_message)
            
            try:
                return response.json()
            except ValueError:
                raise SJMAPIError(f"Invalid JSON response: {response.text}")
            
        except requests.exceptions.RequestException as e:
            raise SJMAPIError(f"Request failed: {str(e)}")
    
    def health(self) -> Dict[str, Any]:
        """
        Check the health of the SJM API.
        
        Returns:
            Dictionary with health status information
            
        Example:
            ```python
            client = SJM(api_key="your_api_key")
            health = client.health()
            print(f"API Status: {health['status']}")
            ```
        """
        return self._request("GET", "/health")
    
    def match(
        self,
        description: str,
        required_skills: List[str],
        budget_range: Tuple[int, int] = (5000, 10000),
        complexity: str = "medium",
        timeline: int = 30
    ) -> Dict[str, Any]:
        """
        Match freelancers to a project based on provided criteria.
        
        Args:
            description: Project description
            required_skills: List of required skills
            budget_range: Tuple of (min, max) budget in USD
            complexity: Project complexity ("low", "medium", "high")
            timeline: Project timeline in days
            
        Returns:
            Dictionary with matching freelancers
            
        Example:
            ```python
            client = SJM(api_key="your_api_key")
            matches = client.match(
                description="Build a modern web application with React",
                required_skills=["React.js", "Node.js", "TypeScript"],
                budget_range=(5000, 10000),
                complexity="medium",
                timeline=30
            )
            
            for match in matches["matches"][:3]:
                freelancer = match["freelancer"]
                print(f"{freelancer['name']} - Score: {match['score']}")
            ```
        """
        data = {
            "description": description,
            "required_skills": required_skills,
            "budget_range": budget_range,
            "complexity": complexity,
            "timeline": timeline
        }
        
        return self._request("POST", "/match", data=data)
    
    def verify_skill(self, keyword: str) -> Dict[str, Any]:
        """
        Verify if a skill exists in the SJM database.
        
        Args:
            keyword: Skill to verify
            
        Returns:
            Dictionary with verification results
            
        Example:
            ```python
            client = SJM(api_key="your_api_key")
            result = client.verify_skill("React.js")
            if result["data"]["exists"]:
                print("Skill exists in the database")
            else:
                print("Skill not found")
                if result["data"]["similar_terms"]:
                    print(f"Did you mean: {', '.join(result['data']['similar_terms'])}")
            ```
        """
        data = {"keyword": keyword}
        return self._request("POST", "/verify-skill", data=data)
    
    def interview(
        self,
        freelancer_id: str,
        project_description: str,
        required_skills: List[str],
        job_title: str,
        mode: str = "ai_questions",
        session_id: Optional[str] = None,
        provided_answers: Optional[List[str]] = None,
        custom_questions: Optional[List[Dict[str, Any]]] = None,
        scoring_criteria: Optional[Dict[str, int]] = None
    ) -> Dict[str, Any]:
        """
        Conduct an interview with a freelancer.
        
        Args:
            freelancer_id: ID of the freelancer
            project_description: Description of the project
            required_skills: List of required skills
            job_title: Job title for the position
            mode: Interview mode ("ai_full", "ai_questions", "custom_full", "hybrid")
            session_id: Optional session ID for continuing an interview
            provided_answers: Optional answers for evaluation
            custom_questions: Optional custom questions (required for custom_full mode)
            scoring_criteria: Optional custom scoring criteria
            
        Returns:
            Dictionary with interview results
            
        Example:
            ```python
            client = SJM(api_key="your_api_key")
            
            # Generate questions
            interview = client.interview(
                freelancer_id="f123",
                project_description="Build a modern web application",
                required_skills=["React", "Node.js"],
                job_title="Full Stack Developer",
                mode="ai_questions"
            )
            
            # Get session ID and questions
            session_id = interview["data"]["session_id"]
            questions = interview["data"]["interview_data"]["questions"]
            
            # Display questions to the user and collect answers
            answers = []
            for q in questions:
                print(f"Q: {q['text']}")
                answer = input("A: ")
                answers.append(answer)
            
            # Submit answers for evaluation
            evaluation = client.interview(
                freelancer_id="f123",
                project_description="Build a modern web application",
                required_skills=["React", "Node.js"],
                job_title="Full Stack Developer",
                mode="ai_full",
                session_id=session_id,
                provided_answers=answers
            )
            
            # Display evaluation
            score = evaluation["data"]["evaluation"]["overall_score"]
            print(f"Overall Score: {score}/100")
            ```
        """
        data = {
            "freelancer_id": freelancer_id,
            "project_description": project_description,
            "required_skills": required_skills,
            "job_title": job_title,
            "mode": mode
        }
        
        if session_id:
            data["session_id"] = session_id
            
        if provided_answers:
            data["provided_answers"] = provided_answers
            
        if custom_questions:
            data["custom_questions"] = custom_questions
            
        if scoring_criteria:
            data["scoring_criteria"] = scoring_criteria
            
        return self._request("POST", "/interview", data=data)
    
    def generate_test_data(self, num_freelancers: int = 100) -> Dict[str, Any]:
        """
        Generate test freelancer data.
        
        Args:
            num_freelancers: Number of freelancers to generate
            
        Returns:
            Dictionary with generated freelancers
            
        Example:
            ```python
            client = SJM(api_key="your_api_key")
            test_data = client.generate_test_data(num_freelancers=10)
            freelancers = test_data["data"]
            print(f"Generated {len(freelancers)} test freelancers")
            ```
        """
        return self._request("GET", f"/generate-test-data?num_freelancers={num_freelancers}")
    
    def parse_resume(self, file_path: str) -> Dict[str, Any]:
        """
        Parse a resume file to extract skills and other information.
        
        Args:
            file_path: Path to the resume file (PDF or DOCX)
            
        Returns:
            Dictionary with parsed resume data
            
        Example:
            ```python
            client = SJM(api_key="your_api_key")
            resume_data = client.parse_resume("resume.pdf")
            skills = resume_data["data"]["skills"]
            print(f"Extracted Skills: {', '.join(skills)}")
            ```
        """
        file_name = os.path.basename(file_path)
        with open(file_path, 'rb') as f:
            files = {'file': (file_name, f)}
            return self._request("POST", "/parse", files=files)
    
    def parse_resume_buffer(self, file_buffer: BinaryIO, file_name: str) -> Dict[str, Any]:
        """
        Parse a resume from a file-like object.
        
        Args:
            file_buffer: File-like object containing the resume
            file_name: Name of the file (including extension)
            
        Returns:
            Dictionary with parsed resume data
        """
        files = {'file': (file_name, file_buffer)}
        return self._request("POST", "/parse", files=files)
