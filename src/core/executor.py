"""
Executor module.

Responsible for executing planned tasks by routing them to the
correct module and collecting their results.
"""

from typing import List, Dict, Any


class Executor:
    def __init__(self, router):
        """
        Initialize the executor.

        Args:
            router: TaskRouter instance used to resolve modules
        """
        self.router = router

    def execute(self, tasks: List[Dict[str, Any]]) -> List[str]:
        """
        Execute tasks sequentially.

        Args:
            tasks: List of tasks produced by the planner

        Task schema:
        {
            "module": str,
            "task": str,
            "parameters": dict
        }

        Returns:
            List[str] results from each module execution
        """

        results = []

        for task in tasks:
            try:
                # 1. Validate basic schema
                if "module" not in task or "task" not in task:
                    raise ValueError(f"Invalid task format: {task}")

                # 2. Route to correct module
                module = self.router.route(task)

                if module is None:
                    raise ValueError(f"No module found for: {task['module']}")

                # 3. Execute task
                result = module.execute(task)

                # 4. Collect result
                results.append(result)

            except Exception as e:
                # Instead of crashing, return error result
                results.append(f"Error executing task {task}: {str(e)}")

        return results