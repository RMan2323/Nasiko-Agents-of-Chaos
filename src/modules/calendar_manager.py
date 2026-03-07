"""
CalendarManager module.

Handles calendar-related tasks using an LLM.
"""

from typing import Dict, Any
from src.core.base_module import BaseModule
from openai import OpenAI
import os


class CalendarManager(BaseModule):

    def __init__(self):
        super().__init__()
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def execute(self, task: Dict[str, Any]) -> str:
        """
        Supported tasks:

        - schedule_event
        - list_events
        - cancel_event
        """

        self.validate_task(task)

        task_name = task["task"]
        parameters = task.get("parameters", {})

        if task_name == "schedule_event":
            prompt = self._build_schedule_prompt(parameters)

        elif task_name == "list_events":
            prompt = self._build_list_prompt(parameters)

        elif task_name == "cancel_event":
            prompt = self._build_cancel_prompt(parameters)

        else:
            raise ValueError(f"Unsupported calendar task: {task_name}")

        return self._call_llm(prompt)

    # -----------------------------------------------------

    def _call_llm(self, prompt: str) -> str:
        response = self.client.responses.create(
            model="gpt-4.1-mini",
            input=prompt
        )

        return response.output_text

    # -----------------------------------------------------

    def _build_schedule_prompt(self, parameters: Dict[str, Any]) -> str:

        title = parameters.get("title")
        time = parameters.get("time")
        date = parameters.get("date")

        return f"""
You are a calendar assistant.

Schedule the following event.

Title: {title}
Date: {date}
Time: {time}

Return a confirmation message including event details.
"""

    # -----------------------------------------------------

    def _build_list_prompt(self, parameters: Dict[str, Any]) -> str:

        date = parameters.get("date", "today")

        return f"""
You are a calendar assistant.

List the scheduled events for {date}.

Return them clearly in bullet points.
"""

    # -----------------------------------------------------

    def _build_cancel_prompt(self, parameters: Dict[str, Any]) -> str:

        title = parameters.get("title")

        return f"""
You are a calendar assistant.

Cancel the following event:

Event title: {title}

Return a confirmation that the event was cancelled.
"""