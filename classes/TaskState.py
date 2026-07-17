import json, ctypes
from os import path

class TaskState:
    def __init__(self):
        if not path.isfile(self._get_resources_path("task_state.json")):
            with open(self._get_resources_path("task_state.json"), "w") as settings_file:
                state_data = {"start_task_created_state": "false"}
                json.dump(state_data, settings_file, indent=4)
    
    def _get_resources_path(self, file: str):
        base_path = path.abspath(".")
        return path.join(base_path, file)

    def mark_task_created(self):
        with open(self._get_resources_path("task_state.json"), "r") as state_file:
            state_data = json.load(state_file)
        with open(self._get_resources_path("task_state.json"), "w") as state_file:
            state_data["start_task_created_state"] = "true"
            json.dump(state_data, state_file, indent=4)
    
    def is_task_already_created(self):
        with open(self._get_resources_path("task_state.json")) as state_file:
            state_data = json.load(state_file)
        if state_data["start_task_created_state"] == "true":
            return True
        else:
            return False
    
    def is_user_admin(self):
        return ctypes.windll.shell32.IsUserAnAdmin() == 1
            
task_state = TaskState()