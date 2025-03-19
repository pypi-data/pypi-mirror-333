"""
SJM AI Client - Utility functions

This module contains utility functions for the SJM client.
"""

import re
from typing import List, Dict, Any


def parse_skills_string(skills_string: str) -> List[str]:
    """
    Parse a comma-separated string of skills into a list.
    
    Args:
        skills_string: Comma-separated string of skills
        
    Returns:
        List of skills with whitespace trimmed
    """
    if not skills_string:
        return []
    return [skill.strip() for skill in skills_string.split(',') if skill.strip()]


def format_budget_range(budget_min: int, budget_max: int) -> str:
    """
    Format a budget range as a human-readable string.
    
    Args:
        budget_min: Minimum budget
        budget_max: Maximum budget
        
    Returns:
        Formatted budget range string
    """
    return f"${budget_min:,} - ${budget_max:,}"


def truncate_text(text: str, max_length: int = 100) -> str:
    """
    Truncate text to a maximum length with ellipsis.
    
    Args:
        text: Text to truncate
        max_length: Maximum length
        
    Returns:
        Truncated text
    """
    if not text or len(text) <= max_length:
        return text
    return text[:max_length-3] + "..."
