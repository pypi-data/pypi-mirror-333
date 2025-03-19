import struct
from typing import Dict, List

from robot_simulator.core.constants import (
    DOUBLE_FORMAT,
    UNSIGNED_CHAR_FORMAT,
    UNSIGNED_SHORT_FORMAT,
    USIGNED_INT,
)


class Encoder:
    def __init__(self):
        self.DOUBLE_FORMAT = DOUBLE_FORMAT
        self.UNSIGNED_CHAR_FORMAT = UNSIGNED_CHAR_FORMAT
        self.USIGNED_INT = USIGNED_INT
        self.UNSIGNED_SHORT_FORMAT = UNSIGNED_SHORT_FORMAT

    def encode_header(
        self,
        header,
    ) -> bytes:
        command_type = struct.pack(self.UNSIGNED_CHAR_FORMAT, header.command_type.value)
        command_id = struct.pack(self.UNSIGNED_CHAR_FORMAT, header.command_id.value)
        error_code = struct.pack(self.UNSIGNED_CHAR_FORMAT, header.error_code.value)
        timestamp = struct.pack(self.DOUBLE_FORMAT, header.timestamp)
        size_of_body = struct.pack(self.UNSIGNED_SHORT_FORMAT, header.size_of_body)

        return command_type + command_id + error_code + timestamp + size_of_body

    def encode_pos(self, pos: List[float]) -> bytes:
        """
        Encode a position.

        Args:
            pos (list): The position to encode.

        Returns:
            bytes: The encoded position.
        """
        return struct.pack(self.DOUBLE_FORMAT * len(pos), *pos)

    def double_bool_to_bytes(self, bool_1: bool, bool_2: bool) -> bytes:
        """
        Return the bytes corresponding to the two booleans.

        Args:
            bool_1 (bool): The first boolean
            bool_2 (bool): The second boolean

        Returns:
            bytes: Corresponding bytes to the two booleans.
        """
        return struct.pack(
            self.UNSIGNED_CHAR_FORMAT,
            sum(1 << i for i, v in enumerate([bool_1, bool_2]) if v),
        )

    def encode_connect_response(self, version: str) -> bytes:
        """
        Encode each version character into double bytes.

        Args:
            version (str): The responses to encode.

        Returns:
            bytes: The encoded version.
        """
        return struct.pack(self.DOUBLE_FORMAT * len(version), *version.encode())

    def encode_getstate_response(self, response: Dict) -> bytes:
        """
        Encode the response to the GETSTATE command.

        Args:
            response (dict): The responses to encode.

        Returns:
            (bytes): The encoded responses.
        """
        cartesian_positions = self.encode_pos(response.get("cartesian_positions"))
        robot_config = struct.pack(
            self.UNSIGNED_CHAR_FORMAT, response.get("robot_config")
        )
        joint_values = self.encode_pos(response.get("joint_values"))
        pedal_status = struct.pack(
            self.UNSIGNED_CHAR_FORMAT, response.get("pedal_status")
        )
        state_machine = struct.pack(
            self.UNSIGNED_CHAR_FORMAT, response.get("state_machine")
        )
        safety_state = struct.pack(
            self.UNSIGNED_CHAR_FORMAT, response.get("safety_state")
        )
        move_id = struct.pack(self.DOUBLE_FORMAT, response.get("move_id"))
        is_settled = self.double_bool_to_bytes(
            response.get("is_settled"), response.get("latch_status")
        )

        return (
            cartesian_positions
            + robot_config
            + joint_values
            + pedal_status
            + state_machine
            + safety_state
            + move_id
            + is_settled
        )

    def encode_getlatchedpose_response(self, response: Dict) -> bytes:
        """
        Encode the responses to the GETLATCHEDPOSE command.

        Args:
            responses (bytes): The responses to encode."""
        cartesian_pos = self.encode_pos(response.get("cartesian_positions"))
        robot_config = struct.pack(
            self.UNSIGNED_CHAR_FORMAT, response.get("robot_config")
        )

        return cartesian_pos + robot_config

    def encode_trajectorymove_response(self, response: Dict) -> bytes:
        cartesian_pos = self.encode_pos(response.get("cartesian_positions"))
        robot_config = struct.pack(
            self.UNSIGNED_CHAR_FORMAT, response.get("robot_config")
        )
        joint_values = self.encode_pos(response.get("joint_values"))
        pedal_status = struct.pack(
            self.UNSIGNED_CHAR_FORMAT, response.get("pedal_status")
        )
        state_machine = struct.pack(
            self.UNSIGNED_CHAR_FORMAT, response.get("state_machine")
        )
        safety_state = struct.pack(
            self.UNSIGNED_CHAR_FORMAT, response.get("safety_state")
        )
        move_id = struct.pack(self.DOUBLE_FORMAT, response.get("move_id"))
        is_settled_latch_status = self.double_bool_to_bytes(
            response.get("is_settled"), response.get("latch_status")
        )
        point_id = struct.pack(self.USIGNED_INT, response.get("point_id"))

        return (
            cartesian_pos
            + robot_config
            + joint_values
            + pedal_status
            + state_machine
            + safety_state
            + move_id
            + is_settled_latch_status
            + point_id
        )
