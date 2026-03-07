from src.core import TaskPlanner

planner = TaskPlanner()

message = "I want to have a meet set on google planning app"

tasks = planner.plan(message)

print(planner.to_json(tasks))