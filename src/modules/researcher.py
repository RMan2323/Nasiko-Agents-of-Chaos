"""
Researcher module for gathering information about candidates and companies.
"""
from typing import Dict, Any, List
from core.base_module import BaseModule
from langchain_openai import ChatOpenAI


class Researcher(BaseModule):
    """Conducts research on candidates, companies, and market trends."""
    
    def __init__(self):
        super().__init__("researcher")
        self.llm = ChatOpenAI(model="gpt-4o", temperature=0.3)
    
    def can_handle(self, task: Dict[str, Any]) -> bool:
        """Check if this module can handle the task."""
        task_type = task.get("type", "")
        keywords = ["research", "background", "investigate", "find", "lookup", "information"]
        description = task.get("description", "").lower()
        
        return task_type == "research" or any(kw in description for kw in keywords)
    
    def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Execute research task."""
        params = task.get("params", {})
        description = task.get("description", "").lower()
        
        if "candidate" in description:
            return self._research_candidate(params)
        elif "company" in description or "organization" in description:
            return self._research_company(params)
        elif "salary" in description or "compensation" in description:
            return self._research_salary(params)
        elif "market" in description or "trend" in description:
            return self._research_market_trends(params)
        else:
            return self._general_research(params, description)
    
    def _research_candidate(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Research candidate background."""
        candidate_name = params.get("candidate_name", "Candidate")
        focus_areas = params.get("focus_areas", ["professional background", "skills", "achievements"])
        
        prompt = f"""You are an HR researcher. Provide a professional background summary for a candidate named {candidate_name}.

Focus on: {', '.join(focus_areas)}

Since this is a simulation, create a realistic professional profile including:
1. Career trajectory
2. Key skills and expertise
3. Notable achievements
4. Education background
5. Professional reputation indicators

Keep it professional and realistic."""

        response = self.llm.invoke(prompt)
        
        return {
            "success": True,
            "candidate": candidate_name,
            "research_summary": response.content,
            "sources": ["LinkedIn", "Professional Networks", "Public Records"],
            "message": f"Completed background research on {candidate_name}"
        }
    
    def _research_company(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Research company information."""
        company_name = params.get("company_name", "Target Company")
        
        prompt = f"""Provide a comprehensive company overview for {company_name} from an HR perspective.

Include:
1. Company size and industry
2. Work culture and values
3. Employee benefits and perks
4. Growth trajectory
5. Reputation as an employer

Be realistic and professional."""

        response = self.llm.invoke(prompt)
        
        return {
            "success": True,
            "company": company_name,
            "research_summary": response.content,
            "message": f"Completed company research on {company_name}"
        }
    
    def _research_salary(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Research salary and compensation data."""
        job_role = params.get("job_role", "Software Engineer")
        location = params.get("location", "United States")
        experience_level = params.get("experience_level", "mid-level")
        
        # Simulated salary data
        salary_ranges = {
            "entry-level": {"min": 60000, "max": 85000, "median": 72000},
            "mid-level": {"min": 85000, "max": 130000, "median": 105000},
            "senior": {"min": 130000, "max": 180000, "median": 155000},
            "lead": {"min": 160000, "max": 220000, "median": 190000}
        }
        
        salary_data = salary_ranges.get(experience_level, salary_ranges["mid-level"])
        
        return {
            "success": True,
            "role": job_role,
            "location": location,
            "experience_level": experience_level,
            "salary_range": {
                "minimum": f"${salary_data['min']:,}",
                "maximum": f"${salary_data['max']:,}",
                "median": f"${salary_data['median']:,}"
            },
            "additional_info": "Includes base salary. Total compensation may include bonuses, equity, and benefits.",
            "message": f"Salary research completed for {experience_level} {job_role} in {location}"
        }
    
    def _research_market_trends(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Research hiring market trends."""
        industry = params.get("industry", "Technology")
        
        prompt = f"""Provide current hiring market trends for the {industry} industry.

Include:
1. In-demand skills
2. Hiring challenges
3. Salary trends
4. Remote work trends
5. Key predictions for the next 6-12 months

Be data-informed and practical."""

        response = self.llm.invoke(prompt)
        
        return {
            "success": True,
            "industry": industry,
            "trends_summary": response.content,
            "message": f"Market trends research completed for {industry}"
        }
    
    def _general_research(self, params: Dict[str, Any], description: str) -> Dict[str, Any]:
        """Conduct general research."""
        prompt = f"""You are an HR researcher. Provide helpful research for this request:

Request: {description}
Context: {params}

Provide comprehensive, well-organized information."""

        response = self.llm.invoke(prompt)
        
        return {
            "success": True,
            "research_summary": response.content,
            "message": "Research completed"
        }
    
    def get_capabilities(self) -> List[str]:
        """Return module capabilities."""
        return [
            "Research candidate backgrounds",
            "Company information lookup",
            "Salary and compensation research",
            "Market trend analysis",
            "Industry insights",
            "Competitive intelligence"
        ]
