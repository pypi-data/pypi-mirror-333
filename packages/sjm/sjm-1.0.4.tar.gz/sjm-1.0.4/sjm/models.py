from dataclasses import dataclass
from typing import List, Dict, Optional, Any, Union

@dataclass
class Freelancer:
    id: str
    name: str
    job_title: str
    skills: List[str]
    experience: int
    rating: float
    hourly_rate: float
    availability: bool
    total_sales: int
    
@dataclass
class Match:
    freelancer: Freelancer
    score: float
    matching_skills: int
    
@dataclass
class HealthStatus:
    status: str
    components: Dict[str, Any]
