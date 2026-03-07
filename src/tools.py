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
def add_candidate_to_database(
    name: str,
    email: str,
    college: str = "",
    cpi: float = 0.0,
    skills: str = "",
    experience_years: int = 0,
    phone: str = "",
    degree: str = ""
) -> str:
    """
    Add a new candidate directly to the MongoDB database.
    
    Args:
        name: Candidate's full name
        email: Candidate's email address (required, unique)
        college: College/University name
        cpi: CPI/GPA score
        skills: Comma-separated skills (e.g., "Python, AWS, React")
        experience_years: Years of experience
        phone: Phone number
        degree: Degree name
    """
    from utils.database import get_database
    
    db = get_database()
    
    # Parse skills
    skills_list = [s.strip() for s in skills.split(",")] if skills else []
    
    candidate_data = {
        "name": name,
        "email": email,
        "college": college,
        "degree": degree,
        "cpi": cpi,
        "skills": skills_list,
        "experience_years": experience_years,
        "phone": phone,
        "status": "applied"
    }
    
    candidate_id = db.add_candidate(candidate_data)
    
    if candidate_id:
        return f"✅ Successfully added candidate {name} (email: {email}) to database with ID: {candidate_id}"
    else:
        return f"❌ Failed to add candidate {name} to database"


@tool
def get_candidate_from_database(email: str) -> str:
    """
    Retrieve candidate information from MongoDB database by email.
    
    Args:
        email: Candidate's email address
    
    Returns:
        Candidate information as formatted string
    """
    from utils.database import get_database
    
    db = get_database()
    candidate = db.get_candidate(email)
    
    if candidate:
        return f"""
Candidate Found in Database:
- Name: {candidate.get('name', 'N/A')}
- Email: {candidate.get('email', 'N/A')}
- College: {candidate.get('college', 'N/A')}
- Degree: {candidate.get('degree', 'N/A')}
- CPI: {candidate.get('cpi', 'N/A')}
- Skills: {', '.join(candidate.get('skills', []))}
- Experience: {candidate.get('experience_years', 0)} years
- Phone: {candidate.get('phone', 'N/A')}
- Status: {candidate.get('status', 'N/A')}
- Screening Score: {candidate.get('screening_score', 'Not screened yet')}
- Culture Fit Score: {candidate.get('culture_fit_score', 'Not analyzed yet')}
"""
    else:
        return f"❌ No candidate found with email: {email}"


@tool
def search_candidates_by_name(name: str) -> str:
    """
    Search for candidates by name (partial match supported).
    Use this when user asks for information about a candidate by name.
    
    Args:
        name: Candidate's name or partial name (e.g., "Bob", "Smith", "Bob Smith")
    
    Returns:
        List of matching candidates with their details
    """
    from utils.database import get_database
    
    db = get_database()
    
    # Search using regex for partial matching (case-insensitive)
    query = {"name": {"$regex": name, "$options": "i"}}
    candidates = db.search_candidates(query)
    
    if not candidates:
        return f"❌ No candidates found with name matching: {name}"
    
    result = f"Found {len(candidates)} candidate(s) matching '{name}':\n\n"
    
    for i, candidate in enumerate(candidates, 1):
        result += f"""
{i}. {candidate.get('name', 'N/A')}
   - Email: {candidate.get('email', 'N/A')}
   - College: {candidate.get('college', 'N/A')}
   - Degree: {candidate.get('degree', 'N/A')}
   - CPI: {candidate.get('cpi', 'N/A')}
   - Skills: {', '.join(candidate.get('skills', []))}
   - Experience: {candidate.get('experience_years', 0)} years
   - Phone: {candidate.get('phone', 'N/A')}
   - Status: {candidate.get('status', 'N/A')}
   - Screening Score: {candidate.get('screening_score', 'Not screened yet')}
"""
    
    return result


@tool
def search_candidates_by_skills(skills: str) -> str:
    """
    Search for candidates who have specific skills.
    Use this when user asks for candidates with particular skills.
    
    Args:
        skills: Comma-separated skills to search for (e.g., "Python, AWS" or "React")
    
    Returns:
        List of candidates with those skills
    """
    from utils.database import get_database
    
    db = get_database()
    
    # Parse skills
    skill_list = [s.strip() for s in skills.split(",")]
    
    # Search for candidates with ANY of the specified skills (case-insensitive)
    query = {
        "skills": {
            "$elemMatch": {
                "$in": [{"$regex": skill, "$options": "i"} for skill in skill_list]
            }
        }
    }
    
    # Simpler approach: use $in with regex
    query = {
        "skills": {
            "$regex": "|".join(skill_list),
            "$options": "i"
        }
    }
    
    candidates = db.search_candidates(query)
    
    if not candidates:
        return f"❌ No candidates found with skills: {skills}"
    
    result = f"Found {len(candidates)} candidate(s) with skills matching '{skills}':\n\n"
    
    for i, candidate in enumerate(candidates, 1):
        matching_skills = [
            s for s in candidate.get('skills', [])
            if any(skill.lower() in s.lower() for skill in skill_list)
        ]
        
        result += f"""
{i}. {candidate.get('name', 'N/A')} ({candidate.get('email', 'N/A')})
   - Matching Skills: {', '.join(matching_skills) if matching_skills else 'N/A'}
   - All Skills: {', '.join(candidate.get('skills', []))}
   - Experience: {candidate.get('experience_years', 0)} years
   - College: {candidate.get('college', 'N/A')}
   - CPI: {candidate.get('cpi', 'N/A')}
   - Status: {candidate.get('status', 'N/A')}
   - Screening Score: {candidate.get('screening_score', 'Not screened yet')}
"""
    
    return result


@tool
def search_candidates_advanced(
    college: str = "",
    min_cpi: float = 0.0,
    min_experience: int = 0,
    status: str = ""
) -> str:
    """
    Advanced search for candidates by multiple criteria.
    
    Args:
        college: College/University name (partial match)
        min_cpi: Minimum CPI/GPA
        min_experience: Minimum years of experience
        status: Candidate status (applied, screened, interviewed, etc.)
    
    Returns:
        List of matching candidates
    """
    from utils.database import get_database
    
    db = get_database()
    
    # Build query
    query = {}
    
    if college:
        query["college"] = {"$regex": college, "$options": "i"}
    
    if min_cpi > 0:
        query["cpi"] = {"$gte": min_cpi}
    
    if min_experience > 0:
        query["experience_years"] = {"$gte": min_experience}
    
    if status:
        query["status"] = status
    
    candidates = db.search_candidates(query)
    
    if not candidates:
        return f"❌ No candidates found matching the criteria"
    
    result = f"Found {len(candidates)} candidate(s) matching criteria:\n\n"
    
    for i, candidate in enumerate(candidates, 1):
        result += f"""
{i}. {candidate.get('name', 'N/A')} ({candidate.get('email', 'N/A')})
   - College: {candidate.get('college', 'N/A')}
   - CPI: {candidate.get('cpi', 'N/A')}
   - Experience: {candidate.get('experience_years', 0)} years
   - Skills: {', '.join(candidate.get('skills', []))}
   - Status: {candidate.get('status', 'N/A')}
   - Screening Score: {candidate.get('screening_score', 'Not screened yet')}
"""
    
    return result


@tool
def schedule_interview(candidate_name: str, interview_type: str = "technical", duration: int = 60, candidate_email: str = "") -> str:
    """
    Schedule an interview with a candidate.
    
    Args:
        candidate_name: Name of the candidate
        interview_type: Type of interview (technical, behavioral, cultural, final)
        duration: Duration in minutes (default 60)
        candidate_email: Candidate's email (optional, for database lookup)
    """
    if not _planner or not _executor or not _aggregator:
        return "Modular system not initialized"
    
    query = f"Schedule a {duration}-minute {interview_type} interview with {candidate_name}"
    if candidate_email:
        query += f", email {candidate_email}"
    
    tasks = _planner.plan(query)
    results = _executor.execute(tasks)
    return _aggregator.combine(results)


@tool
def screen_candidate(candidate_email: str, job_role: str, resume_summary: str = "") -> str:
    """
    Screen and evaluate a candidate for a position.
    First retrieves candidate data from database, then performs screening.
    
    Args:
        candidate_email: Candidate's email address
        job_role: Position they're applying for
        resume_summary: Brief summary of their resume/background (optional if in database)
    """
    from utils.database import get_database
    
    # Get candidate from database first
    db = get_database()
    candidate = db.get_candidate(candidate_email)
    
    if candidate:
        # Build resume summary from database
        resume_summary = f"""
{candidate.get('name', 'Candidate')} from {candidate.get('college', 'Unknown')} with {candidate.get('experience_years', 0)} years of experience.
Skills: {', '.join(candidate.get('skills', []))}
CPI: {candidate.get('cpi', 'N/A')}
Degree: {candidate.get('degree', 'N/A')}
"""
    
    if not _planner or not _executor or not _aggregator:
        return "Modular system not initialized"
    
    query = f"Screen candidate {candidate_email} for {job_role} position. Resume: {resume_summary}"
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
def analyze_culture_fit(candidate_name: str, company_name: str = "our company", candidate_email: str = "") -> str:
    """
    Analyze culture fit between a candidate and company.
    
    Args:
        candidate_name: Name of the candidate
        company_name: Name of the company (default: "our company")
        candidate_email: Candidate's email (optional, for database lookup)
    """
    if not _planner or not _executor or not _aggregator:
        return "Modular system not initialized"
    
    query = f"Analyze culture fit between {candidate_name} and {company_name}"
    if candidate_email:
        query += f", candidate email {candidate_email}"
    
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
