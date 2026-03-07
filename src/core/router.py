from src.modules import CalendarManager, Recruiter, Researcher

class TaskRouter:

    def __init__(self):

        self.modules = {
            "calendar": CalendarManager(),
            "recruiter": Recruiter(),
            "research": Researcher()
        }

    def route(self, task):

        module_name = task["module"]

        return self.modules.get(module_name)