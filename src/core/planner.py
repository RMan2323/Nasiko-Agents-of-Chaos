import json
from openai import OpenAI


ALLOWED_MODULES = {"calendar", "recruiter", "research"}

MODULE_TASKS = {
    "calendar": [
        "schedule_event",
        "list_events",
        "cancel_event"
    ],
    "recruiter": [
        "find_candidates",
        "evaluate_candidate",
        "generate_interview_questions"
    ],
    "research": [
        "find_papers",
        "summarize_topic",
        "search_web"
    ]
}


class TaskPlanner:

    def __init__(self, api_key=None):

        if api_key:
            self.client = OpenAI(api_key=api_key)
        else:
            self.client = OpenAI()

    def _build_prompt(self, message: str):

        return f"""
You are an AI task planner.

Your job is to convert a user request into structured tasks.

STRICT RULES:

1. Output ONLY valid JSON
2. Output must follow this schema

[
  {{
    "module": str,
    "task": str,
    "parameters": dict
  }}
]

3. Use ONLY the allowed modules and tasks.

MODULES AND TASKS:

calendar
- schedule_event
- list_events
- cancel_event

recruiter
- find_candidates
- evaluate_candidate
- generate_interview_questions

research
- find_papers
- summarize_topic
- search_web

IMPORTANT:

• task MUST exactly match one of the supported tasks
• never invent task names
• parameters must contain required info if relevant

Example:

User: Find papers about transformers

Output:

[
  {{
    "module": "research",
    "task": "find_papers",
    "parameters": {{"topic": "transformers"}}
  }}
]

User message:
{message}

Output JSON only.
"""

    def _validate_tasks(self, tasks):

        validated = []

        for task in tasks:

            if "module" not in task:
                raise ValueError("Task missing 'module' field")

            module = task["module"]

            if module not in ALLOWED_MODULES:
                raise ValueError(f"Invalid module: {module}")

            if "task" not in task:
                raise ValueError("Task missing 'task' field")

            task_name = task["task"]

            if task_name not in MODULE_TASKS[module]:
                raise ValueError(
                    f"Unsupported task '{task_name}' for module '{module}'"
                )

            if "parameters" not in task:
                task["parameters"] = {}

            validated.append(task)

        return validated

    def _extract_json(self, text: str):

        """
        Extract JSON from LLM response safely.
        """

        text = text.strip()

        # remove markdown blocks if present
        if text.startswith("```"):
            text = text.split("```")[1]

        return json.loads(text)

    def plan(self, message: str):

        prompt = self._build_prompt(message)

        response = self.client.responses.create(
            model="gpt-4.1-mini",
            input=prompt,
            temperature=0
        )

        text = response.output[0].content[0].text

        try:
            tasks = self._extract_json(text)
        except Exception:
            raise ValueError(
                f"Planner returned invalid JSON:\n{text}"
            )

        tasks = self._validate_tasks(tasks)

        return tasks

    def to_json(self, tasks):

        return json.dumps(tasks, indent=2)