"""
Researcher module.

Handles research-related tasks using an LLM.
"""

from typing import Dict, Any
from src.core.base_module import BaseModule
from openai import OpenAI
import os


class Researcher(BaseModule):
    """
    Research module powered by OpenAI LLM.
    """

    def __init__(self):
        super().__init__()
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def execute(self, task: Dict[str, Any]) -> str:
        """
        Execute research tasks.

        Supported tasks:
        - find_papers
        - summarize_topic
        - search_web
        """

        # Validate task structure
        self.validate_task(task)

        task_name = task["task"]
        parameters = task.get("parameters", {})

        if task_name == "find_papers":
            prompt = self._build_find_papers_prompt(parameters)

        elif task_name == "summarize_topic":
            prompt = self._build_summarize_prompt(parameters)

        elif task_name == "search_web":
            prompt = self._build_search_prompt(parameters)

        else:
            raise ValueError(f"Unsupported research task: {task_name}")

        return self._call_llm(prompt)

    # -----------------------------------------------------

    def _call_llm(self, prompt: str) -> str:
        """
        Call OpenAI model to generate output.
        """

        response = self.client.responses.create(
            model="gpt-4.1-mini",
            input=prompt,
        )

        return response.output_text

    # -----------------------------------------------------

    def _build_find_papers_prompt(self, parameters: Dict[str, Any]) -> str:
        topic = parameters.get("topic")

        if not topic:
            raise ValueError("find_papers requires 'topic' parameter")

        return f"""
You are an academic research assistant.

Find important research papers related to the topic below.

Topic: {topic}

Return:
- paper title
- authors
- short description
"""

    # -----------------------------------------------------

    def _build_summarize_prompt(self, parameters: Dict[str, Any]) -> str:
        topic = parameters.get("topic")

        if not topic:
            raise ValueError("summarize_topic requires 'topic' parameter")

        return f"""
Explain the following topic in a clear concise summary.

Topic: {topic}

Include:
- key concepts
- main applications
- recent developments
"""

    # -----------------------------------------------------

    def _build_search_prompt(self, parameters: Dict[str, Any]) -> str:
        query = parameters.get("query")

        if not query:
            raise ValueError("search_web requires 'query' parameter")

        return f"""
Provide relevant information for the following web search query.

Query: {query}

Return:
- key information
- recent updates
- useful resources
"""