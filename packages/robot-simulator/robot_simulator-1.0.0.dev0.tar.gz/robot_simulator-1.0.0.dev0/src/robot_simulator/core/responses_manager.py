from typing import Any, Dict, List, Union

from robot_simulator.core.commands import MainCommandId, MoveCommandId
from robot_simulator.core.logger_manager import Logger
from robot_simulator.core.responses import Responses
from robot_simulator.core.utils import update_dict_value


class ResponsesManager:
    MAIN_KEY = "main"
    TRAJECTORY_KEY = "trajectory"

    def __init__(self, default_responses: Dict):
        self.default_responses = default_responses
        self.logger = Logger()
        self.logger.log_info(f"Load default responses: {self.default_responses}")
        self.responses = self.find_responses()

    def _get_main_connect(self):
        return self.default_responses[self.MAIN_KEY].get("1", {}).get("version", "")

    def _get_main_getstate(self):
        return self.default_responses[self.MAIN_KEY].get("5", {})

    def _get_main_getlatchedpose(self):
        return self.default_responses[self.MAIN_KEY].get("6", {})

    def _get_trajectory_move(self):
        return self.default_responses[self.TRAJECTORY_KEY].get("2", {})

    def _find_responses(
        self, command_type: str, command_id: Union[str, int]
    ) -> Union[Dict, List[Dict]]:
        command_lookup = {
            (self.MAIN_KEY, MainCommandId.CONNECT): self._get_main_connect,
            (self.MAIN_KEY, MainCommandId.GETSTATE): self._get_main_getstate,
            (
                self.MAIN_KEY,
                MainCommandId.GETLATCHEDPOSE,
            ): self._get_main_getlatchedpose,
            (
                self.TRAJECTORY_KEY,
                MoveCommandId.TRAJECTORYMOVE,
            ): self._get_trajectory_move,
        }
        return command_lookup.get((command_type, command_id), lambda: {})()

    def find_responses(self) -> "Responses":
        return Responses(
            connect=self._find_responses(self.MAIN_KEY, MainCommandId.CONNECT),
            getstate=self._find_responses(self.MAIN_KEY, MainCommandId.GETSTATE),
            getlatchedpose=self._find_responses(
                self.MAIN_KEY, MainCommandId.GETLATCHEDPOSE
            ),
            trajectorymove=self._find_responses(
                self.TRAJECTORY_KEY, MoveCommandId.TRAJECTORYMOVE
            ),
        )

    def update_responses(self, updates: List[Dict[str, Any]]):
        """
        Update multiple nested dictionary values given a list of updates.
        Each update is a dictionary with keys: 'type', 'id', 'key', 'value', and optionally 'index'.
        """
        for update in updates:
            update_type = update["type"]
            update_id = update["id"]
            key = update["key"]
            value = update["value"]
            index = update.get("index", None)

            # Navigate to the correct sub-dictionary
            d = self.default_responses.setdefault(update_type, {})
            d = d.setdefault(update_id, {})

            update_dict_value(d, key, index, value)

        self._apply_updates()

    def _apply_updates(self):
        self.responses = self.find_responses()
