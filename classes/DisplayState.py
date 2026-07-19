import json, threading
from os import path
from .DisplayManager import display_manager

class DisplayState:
    def __init__(self):
        self.windows_watchdog_enabled = True
        self.previous_app_active: bool | None = None
        self._lock = threading.Lock()
        self.initialize_display_configuration()

    def initialize_display_configuration(self):
        if not path.isfile(self._get_resources_path("display_settings.json")):
            with open(self._get_resources_path("display_settings.json"), "w") as settings_file:
                settings_data = {"default_display_mode": "extend", "native_apps": [], "browser_sites": []}
                json.dump(settings_data, settings_file, indent=4)
            self.change_display_mode("extend")
        if not path.isfile(self._get_resources_path("display_state.json")):
            with open(self._get_resources_path("display_state.json"), "w") as state_file:
                state_data = {"display_state": "extend"}
                json.dump(state_data, state_file, indent=4)
     
    def _get_resources_path(self, file: str):
        base_path = path.abspath(".")
        return path.join(base_path, file)

    def get_default_display_mode(self):
        with open(self._get_resources_path("display_settings.json"), "r") as settings_file:
            default_display_mode = json.load(settings_file)["default_display_mode"]
        return default_display_mode.lower()
    
    def get_current_display_state(self):
        with self._lock:
            current_display_state = json.load(open(self._get_resources_path("display_state.json")))["display_state"]
            return current_display_state.lower()
    
    def _save_display_state(self, state: str):
        with open(self._get_resources_path("display_state.json"), "w") as state_file:
            new_display_state = {"display_state": state}
            json.dump(new_display_state, state_file, indent=4)
            
    def change_display_mode(self, display_mode: str):
        with self._lock:
            self._save_display_state(display_mode)
            getattr(display_manager, display_mode)()
    
display_state = DisplayState()