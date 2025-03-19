from typing import Any, Dict, List

from robot_simulator.core.settings import Settings
from robot_simulator.core.utils import update_dict_value


class SettingsManager:
    SETTINGS_KEY = "settings"
    LATENCY_KEY = "latency"

    def __init__(self, default_settings: Dict):
        self.settings_data = default_settings
        self._load_default_settings(self.settings_data)

    def _load_default_settings(self, default_settings: Dict):
        self.settings = Settings(latency=default_settings.get(self.LATENCY_KEY))

    def update_settings(self, updates: List[Dict[str, Any]]):
        """
        Update multiple settings values given a list of updates.
        Each update is a dictionary with keys: 'type', 'key', 'value', and optionally 'index'.
        """
        for update in updates:
            key = update["key"]
            value = update["value"]
            index = update.get("index", None)

            update_dict_value(self.settings_data, key, index, value)

        self._load_default_settings(self.settings_data)
