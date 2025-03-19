# SJM

[![PyPI version](https://img.shields.io/pypi/v/sjm.svg)](https://pypi.org/project/sjm/)
[![Python versions](https://img.shields.io/pypi/pyversions/sjm.svg)](https://pypi.org/project/sjm/)
[![License](https://img.shields.io/pypi/l/sjm.svg)](https://github.com/snapjobsai/sjm-python-client/blob/main/LICENSE)

Official Python client for the SJM (Snap Job Model) API - a powerful AI-driven freelancer matching and recruitment system.

## 🚀 Features

- **Freelancer Matching**: Find the perfect talent for your projects with advanced AI matching
- **Skills Verification**: Validate and verify skills against our extensive database
- **AI-Powered Interviews**: Conduct automated interviews with robust evaluation
- **Resume Parsing**: Extract skills and information from resumes
- **Comprehensive client**: Clean, Pythonic interface to all SJM API endpoints
- **Command-line interface**: Access SJM capabilities from your terminal
- **Robust error handling**: Detailed exceptions with comprehensive information

## 🏠 Installation

```bash
pip install sjm
```

## 🔑 Authentication

To use the SJM client, you'll need an API key from SnapJobsAI. [Contact us](https://snapjobsai.com) to obtain your API key.

## 📚 Quick Start

```python
from sjm import SJM

# Initialize client with your API key
client = SJM(api_key="your_api_key")

# Check API health
health = client.health()
print(f"API Status: {health['status']}")

# Match freelancers to a project
matches = client.match(
    description="Build a modern web application with React and Node.js",
    required_skills=["React.js", "Node.js", "TypeScript"],
    budget_range=(5000, 10000),
    complexity="medium",
    timeline=30
)

# Display top matches
for match in matches["matches"][:3]:
    freelancer = match["freelancer"]
    print(f"Match: {freelancer['name']} ({freelancer['job_title']})")
    print(f"Score: {match['score']:.2f}")
    print(f"Matching Skills: {match['matching_skills']}")
    print(f"Hourly Rate: ${freelancer['hourly_rate']}/hr")
    print("---")
```

## 📋 Example: AI Interviews

```python
from sjm import SJM

client = SJM(api_key="your_api_key")

# Generate interview questions
interview = client.interview(
    freelancer_id="f123",
    project_description="Build a modern web application with React",
    required_skills=["React.js", "Node.js", "TypeScript"],
    job_title="Full Stack Developer",
    mode="ai_questions"
)

# Get session ID and questions
session_id = interview["data"]["session_id"]
questions = interview["data"]["interview_data"]["questions"]

# Display questions to collect answers
answers = []
for i, q in enumerate(questions, 1):
    print(f"Q{i}: {q['text']}")
    answer = input("Answer: ")
    answers.append(answer)

# Submit answers for evaluation
evaluation = client.interview(
    freelancer_id="f123",
    project_description="Build a modern web application with React",
    required_skills=["React.js", "Node.js", "TypeScript"],
    job_title="Full Stack Developer",
    mode="ai_full",
    session_id=session_id,
    provided_answers=answers
)

# Display evaluation results
if "evaluation" in evaluation["data"]:
    eval_data = evaluation["data"]["evaluation"]
    print(f"Overall Score: {eval_data['overall_score']}/100")
    print(f"Strengths: {', '.join(eval_data['strengths'])}")
    print(f"Areas for Improvement: {', '.join(eval_data['areas_for_improvement'])}")
    print(f"Hiring Recommendation: {'Yes' if eval_data['hiring_recommendation'] else 'No'}")
```

## 🖥️ Command Line Interface

The package includes a CLI for convenient access to SJM API functionality:

```bash
# Set your API key as an environment variable (recommended)
export SJM_API_KEY="your_api_key"

# Check API health
sjm health

# Match freelancers to a project
sjm match --description "Web development project" --skills "React.js,Node.js,TypeScript"

# Verify if a skill exists in the database
sjm verify "React.js"

# Generate test data
sjm generate --count 10

# Display help
sjm --help
```

## 📖 API Reference

### Client Initialization

```python
from sjm import SJM

# Basic initialization
client = SJM(api_key="your_api_key")

# Custom base URL (if needed)
client = SJM(
    api_key="your_api_key",
    base_url="https://your-custom-endpoint.com/api/v1/docker"
)
```

### Available Methods

| Method | Description |
|--------|-------------|
| `health()` | Check the health status of the SJM API |
| `match(description, required_skills, ...)` | Match freelancers to a project |
| `verify_skill(keyword)` | Verify if a skill exists in the database |
| `interview(freelancer_id, project_description, ...)` | Conduct an AI interview |
| `generate_test_data(num_freelancers)` | Generate test freelancer data |
| `parse_resume(file_path)` | Parse a resume file to extract skills |

For detailed documentation on each method, please refer to the [full API documentation](https://snapjobsai.com/docs).

## ⚙️ Error Handling

The client provides detailed exception handling for different error scenarios:

```python
from sjm import SJM, SJMAuthenticationError, SJMRateLimitError, SJMAPIError

client = SJM(api_key="your_api_key")

try:
    result = client.match(
        description="Project description",
        required_skills=["React.js", "Node.js"]
    )
except SJMAuthenticationError as e:
    print(f"Authentication failed: {e}")
except SJMRateLimitError as e:
    print(f"Rate limit exceeded. Reset in {e.reset_at} seconds")
except SJMAPIError as e:
    print(f"API error: {e}")
```

## 🔒 Authentication & Rate Limiting

- API keys are required for all requests
- Rate limiting applies based on your plan:
  - **Freelancer**: Limited requests
  - **Professional**: Higher limits
  - **Enterprise**: Unlimited access
- The client automatically handles rate limit headers and provides appropriate exceptions

## 📞 Support

For questions, issues, or feature requests, please contact [support@snapjobsai.com](mailto:snappyjob.ai@gmail.com) or visit our [website](https://snapjobsai.com).

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
