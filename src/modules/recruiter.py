"""
Recruiter module.

Handles recruitment-related tasks using an LLM.
"""

from typing import Dict, Any
from src.core.base_module import BaseModule
from openai import OpenAI
import os


class Recruiter(BaseModule):

    def __init__(self):
        super().__init__()
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def execute(self, task: Dict[str, Any]) -> str:
        """
        Supported tasks:

        - find_candidates
        - evaluate_candidate
        - generate_interview_questions
        """

        self.validate_task(task)

        task_name = task["task"]
        parameters = task.get("parameters", {})

        if task_name == "find_candidates":
            prompt = self._build_find_candidates_prompt(parameters)

        elif task_name == "evaluate_candidate":
            prompt = self._build_evaluate_prompt(parameters)

        elif task_name == "generate_interview_questions":
            prompt = self._build_questions_prompt(parameters)

        else:
            raise ValueError(f"Unsupported recruiter task: {task_name}")

        return self._call_llm(prompt)

    # -----------------------------------------------------

    def _call_llm(self, prompt: str) -> str:
        response = self.client.responses.create(
            model="gpt-4.1-mini",
            input=prompt
        )

        return response.output_text

    # -----------------------------------------------------

    def _build_find_candidates_prompt(self, parameters: Dict[str, Any]) -> str:

        role = parameters.get("role")
        skills = parameters.get("skills")

        return f"""
You are a technical recruiter.

Find potential candidates for the following role.

Role: {role}
Required skills: {skills}

Return a list of potential candidate profiles with:
- name
- background
- skills
"""

    # -----------------------------------------------------

    def _build_evaluate_prompt(self, parameters: Dict[str, Any]) -> str:

        resume = parameters.get("resume")
        role = parameters.get("role")

        return f"""
You are a recruiter evaluating a candidate.

Role: {role}

Candidate Resume:
{resume}

Evaluate the candidate and provide:

- strengths
- weaknesses
- hiring recommendation
"""

    # -----------------------------------------------------

    def _build_questions_prompt(self, parameters: Dict[str, Any]) -> str:

        role = parameters.get("role")
        skills = parameters.get("skills")

        return f"""
You are a hiring manager preparing interview questions.

Role: {role}
Skills: {skills}

Generate technical interview questions to evaluate the candidate.
"""