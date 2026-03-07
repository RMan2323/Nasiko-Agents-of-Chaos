import json
from openai import OpenAI

ALLOWED_MODULES = {"calendar", "recruiter", "research"}


class TaskPlanner:

    def __init__(self, api_key=None):

        # initialize OpenAI client
        if api_key:
            self.client = OpenAI(api_key=api_key)
        else:
            self.client = OpenAI()

    def _build_prompt(self, message: str):

        return f"""
You are a task planner AI.

Convert the user message into tasks.

Return ONLY JSON.

Schema:

[
 {{
   "module": str,
   "task": str,
   "parameters": dict
 }}
]

Allowed modules:
calendar
recruiter
research

User message:
{message}

Output JSON only.
"""

    def _validate_tasks(self, tasks):

        validated = []

        for task in tasks:

            if "module" not in task:
                raise ValueError("Task missing 'module' field")

            if task["module"] not in ALLOWED_MODULES:
                raise ValueError(
                    f"Unrecognized module: {task['module']}"
                )

            if "task" not in task:
                raise ValueError("Task missing 'task' field")

            if "parameters" not in task:
                task["parameters"] = {}

            validated.append(task)

        return validated

    def plan(self, message: str):

        prompt = self._build_prompt(message)

        response = self.client.responses.create(
            model="gpt-4.1-mini",
            input=prompt
        )

        text = response.output[0].content[0].text

        try:
            tasks = json.loads(text)
        except Exception:
            raise ValueError("Planner returned invalid JSON")

        tasks = self._validate_tasks(tasks)

        return tasks

    def to_json(self, tasks):

        return json.dumps(tasks, indent=2)