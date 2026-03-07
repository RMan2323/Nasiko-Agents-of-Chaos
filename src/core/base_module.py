"""
Base module interface for all agent modules.

Every functional module (Researcher, Recruiter, CalendarManager, etc.)
must inherit from this class and implement the execute() method.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any


class BaseModule(ABC):
    """
    Abstract base class for all modules.
    """

    def __init__(self):
        self.name = self.__class__.__name__

    @abstractmethod
    def execute(self, task: Dict[str, Any]) -> str:
        """
        Execute a task assigned to this module.

        Args:
            task (dict): Task dictionary with structure:

                {
                    "module": str,
                    "task": str,
                    "parameters": dict
                }

        Returns:
            str: Result of the task execution
        """
        pass

    def validate_task(self, task: Dict[str, Any]) -> None:
        """
        Validate the task format before execution.
        Raises an error if the format is incorrect.
        """

        if not isinstance(task, dict):
            raise ValueError("Task must be a dictionary.")

        if "task" not in task:
            raise ValueError("Task dictionary must contain 'task' field.")

        if "parameters" not in task:
            raise ValueError("Task dictionary must contain 'parameters' field.")

    def __repr__(self) -> str:
        return f"<Module {self.name}>"