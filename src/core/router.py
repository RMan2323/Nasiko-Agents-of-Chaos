"""
TaskRouter

Responsible for mapping module names to module classes and
returning the correct module instance.
"""

from src.modules import CalendarManager
from src.modules import Recruiter
from src.modules import Researcher


class TaskRouter:
    """
    Routes tasks to the correct module.
    """

    def __init__(self):
        # Registry of module name -> module instance
        self.module_registry = {
            "calendar": CalendarManager(),
            "recruiter": Recruiter(),
            "research": Researcher(),
        }

    def route(self, task: dict):
        """
        Returns the correct module instance for a given task.

        Args:
            task (dict):
            {
                "module": str,
                "task": str,
                "parameters": dict
            }

        Returns:
            module instance
        """

        module_name = task.get("module")

        if module_name is None:
            raise ValueError("Task missing 'module' field")

        if module_name not in self.module_registry:
            raise ValueError(f"Unknown module: {module_name}")

        return self.module_registry[module_name]