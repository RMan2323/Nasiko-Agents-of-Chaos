"""
Tools for the HR agent.
Define your LangChain tools here.
"""
from typing import List, Dict, Any
from langchain_core.tools import tool

# Global references to modular components (set by agent)
_planner = None
_executor = None
_aggregator = None


def set_modular_components(planner, executor, aggregator):
    """Set the modular components for tools to use."""
    global _planner, _executor, _aggregator
    _planner = planner
    _executor = executor
    _aggregator = aggregator


@tool
def schedule_interview(candidate_name: str, date_time: str = "", interview_type: str = "technical", duration: int = 60) -> str:
    """
    Schedule an interview with a candidate.
    
    Args:
        candidate_name: Name of the candidate
        date_time: Requested date and time in ISO format (e.g., '2026-03-15T15:00:00'). Leave empty for next available slot.
        interview_type: Type of interview (technical, behavioral, cultural, final)
        duration: Duration in minutes (default 60)
    """
    if not _planner or not _executor or not _aggregator:
        return "Modular system not initialized"
    
    query = f"Schedule a {duration}-minute {interview_type} interview with {candidate_name}"
    
    # If the AI provided a date/time, append it to the task query
    if date_time:
        query += f" at {date_time}"
        
    tasks = _planner.plan(query)
    
    # Safely inject date_time directly into the planned task parameters to ensure it isn't lost
    for task in tasks:
        if "params" not in task:
            task["params"] = {}
        if date_time:
            task["params"]["date_time"] = date_time
            
    results = _executor.execute(tasks)
    return _aggregator.combine(results)


@tool
def screen_candidate(candidate_name: str, job_role: str, resume_summary: str = "") -> str:
    """
    Screen and evaluate a candidate for a position.
    
    Args:
        candidate_name: Name of the candidate
        job_role: Position they're applying for
        resume_summary: Brief summary of their resume/background
    """
    if not _planner or not _executor or not _aggregator:
        return "Modular system not initialized"
    
    query = f"Screen candidate {candidate_name} for {job_role} position. Resume: {resume_summary}"
    tasks = _planner.plan(query)
    results = _executor.execute(tasks)
    return _aggregator.combine(results)


@tool
def research_candidate(candidate_name: str, focus_areas: str = "professional background") -> str:
    """
    Research a candidate's background and qualifications.
    
    Args:
        candidate_name: Name of the candidate to research
        focus_areas: What to focus on (e.g., "technical skills", "leadership experience")
    """
    if not _planner or not _executor or not _aggregator:
        return "Modular system not initialized"
    
    query = f"Research {candidate_name}'s {focus_areas}"
    tasks = _planner.plan(query)
    results = _executor.execute(tasks)
    return _aggregator.combine(results)


@tool
def get_interview_prep(job_role: str, interview_type: str = "technical", difficulty: str = "medium") -> str:
    """
    Get interview preparation materials including questions and tips.
    
    Args:
        job_role: The position being interviewed for
        interview_type: Type of interview (technical, behavioral, cultural)
        difficulty: Question difficulty (easy, medium, hard)
    """
    if not _planner or not _executor or not _aggregator:
        return "Modular system not initialized"
    
    query = f"Generate {difficulty} {interview_type} interview prep for {job_role}"
    tasks = _planner.plan(query)
    results = _executor.execute(tasks)
    return _aggregator.combine(results)


@tool
def analyze_culture_fit(candidate_name: str, company_name: str = "our company") -> str:
    """
    Analyze culture fit between a candidate and company.
    
    Args:
        candidate_name: Name of the candidate
        company_name: Name of the company (default: "our company")
    """
    if not _planner or not _executor or not _aggregator:
        return "Modular system not initialized"
    
    query = f"Analyze culture fit between {candidate_name} and {company_name}"
    tasks = _planner.plan(query)
    results = _executor.execute(tasks)
    return _aggregator.combine(results)


@tool
def research_salary(job_role: str, location: str = "United States", experience_level: str = "mid-level") -> str:
    """
    Research salary ranges for a position.
    
    Args:
        job_role: The job title/role
        location: Geographic location
        experience_level: Experience level (entry-level, mid-level, senior, lead)
    """
    if not _planner or not _executor or not _aggregator:
        return "Modular system not initialized"
    
    query = f"Research salary for {experience_level} {job_role} in {location}"
    tasks = _planner.plan(query)
    results = _executor.execute(tasks)
    return _aggregator.combine(results)


@tool
def hr_assistant(query: str) -> str:
    """
    General HR assistant for complex multi-step tasks.
    Use this for tasks that don't fit other specific tools or require multiple steps.
    
    Args:
        query: The HR-related question or task
    """
    if not _planner or not _executor or not _aggregator:
        return "Modular system not initialized"
    
    tasks = _planner.plan(query)
    results = _executor.execute(tasks)
    return _aggregator.combine(results)
