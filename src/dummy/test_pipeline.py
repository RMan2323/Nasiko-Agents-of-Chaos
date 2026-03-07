from src.core import TaskPlanner
from src.core import TaskRouter
from src.core import Executor
from src.core import ResultAggregator


def main():

    print("===== TESTING MODULAR AGENT PIPELINE =====\n")

    # Simulated user message
    user_message = "What are your skills?"

    # Initialize components
    planner = TaskPlanner()
    router = TaskRouter()
    executor = Executor(router)
    aggregator = ResultAggregator()

    # Step 1: Plan tasks
    print("Step 1: Running Planner...\n")
    tasks = planner.plan(user_message)
    print("Planned Tasks:")
    print(tasks)
    print("\n")

    # Step 2: Execute tasks
    print("Step 2: Running Executor...\n")
    results = executor.execute(tasks)
    print("Execution Results:")
    # print(results)
    print("\n")

    # Step 3: Aggregate results
    print("Step 3: Running Aggregator...\n")
    final_response = aggregator.combine(results)
    print("Final Response:")
    print(final_response)

    print("\n===== TEST COMPLETE =====")


if __name__ == "__main__":
    main()