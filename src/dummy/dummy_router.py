from src.core import TaskRouter

router = TaskRouter()

task = {
    "module": "calendar",
    "task": "find_papers",
    "parameters": {"topic": "AI"}
}

module = router.route(task)

print(module.__class__.__name__)