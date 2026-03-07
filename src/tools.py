"""
Tools for the agent.
Define your LangChain tools here.
"""
from typing import List, Dict, Any
from langchain_core.tools import tool

# Import modular components
from src.core.planner import TaskPlanner
from src.core.router import TaskRouter
from src.core.executor import Executor
from src.core.aggregator import ResultAggregator


# Initialize modular system once
planner = TaskPlanner()
router = TaskRouter()
executor = Executor(router)
aggregator = ResultAggregator()


@tool
def modular_agent(query: str) -> str:
    """
    Execute complex tasks using the modular architecture.
    Use this tool when the task requires research, scheduling, or recruitment tasks.
    """

    tasks = planner.plan(query)

    results = executor.execute(tasks)

    return aggregator.combine(results)


# Example tool
@tool
def example_tool(param1: str, param2: int) -> str:
    """
    Example tool description.
    
    Args:
        param1: Description of param1
        param2: Description of param2
    """

    return f"Executed example_tool with {param1} and {param2}"