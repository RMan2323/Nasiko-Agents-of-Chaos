from src.core import Executor
from src.core import ResultAggregator


class DummyModule:
    def execute(self, task):
        return f"[DummyModule] Executed task: {task['task']} with parameters {task['parameters']}"


class DummyRouter:
    """
    Simple router for testing that always returns DummyModule
    """

    def route(self, task):
        return DummyModule()


def run_dummy_test():

    # Dummy tasks (simulate planner output)
    tasks = [
        {
            "module": "research",
            "task": "find_papers",
            "parameters": {"topic": "LLM"}
        },
        {
            "module": "calendar",
            "task": "schedule_meeting",
            "parameters": {"time": "3pm"}
        }
    ]

    router = DummyRouter()
    executor = Executor(router)
    aggregator = ResultAggregator()

    results = executor.execute(tasks)

    final_output = aggregator.combine(results)

    print("\n--- FINAL RESPONSE ---\n")
    print(final_output)


if __name__ == "__main__":
    run_dummy_test()