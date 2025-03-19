import struct
from typing import Tuple

from robot_simulator.core.commands import (
    CancelMotion,
    CartesianMove,
    Command,
    CommandType,
    Connect,
    ErrorCode,
    GetLatchPose,
    GetState,
    Header,
    InitializeTrajectory,
    JointMove,
    MainCommandId,
    MoveCommandId,
    SocketType,
    TrajectoryMove,
)
from robot_simulator.core.constants import (
    DOUBLE_FORMAT,
    HEADER_SIZE,
    UNSIGNED_CHAR_FORMAT,
    UNSIGNED_SHORT_FORMAT,
    USIGNED_INT,
)


class DecodeCommand:
    def __init__(self, data: bytes, socket: SocketType):
        self.data = data
        self.socket = socket

        # Constants
        self.HEADER_SIZE = HEADER_SIZE
        self.UNSIGNED_CHAR_FORMAT = UNSIGNED_CHAR_FORMAT
        self.UNSIGNED_SHORT_FORMAT = UNSIGNED_SHORT_FORMAT
        self.DOUBLE_FORMAT = DOUBLE_FORMAT
        self.USIGNED_INT = USIGNED_INT
        self.POS_FORMAT = "6d"
        self.LATCH_ACTIVATION_FORMAT = "1?"
        self.POS_SIZE = 48  # 6 * 8 bytes = 48 bytes
        self.ROBOT_CONFIG_SIZE = 1  # 1 * 1 byte = 1 byte
        self.LINEAR_SPEED_SIZE = 8  # 1 * 8 bytes = 8 bytes
        self.ROTATION_SPEED_SIZE = 8  # 1 * 8 bytes = 8 bytes
        self.POINT_ID_SIZE = 4  # 1 * 4 bytes = 4 bytes
        self.LATCH_ACTIVATION_SIZE = 1  # 1 * 1 byte = 1 byte

    def decode_header(self) -> Header:
        """
        Decode the header of a command from the received data.

        Returns:
            Header: The decoded command header.
        """
        command_type = struct.unpack(self.UNSIGNED_CHAR_FORMAT, self.data[0:1])[0]
        command_id = struct.unpack(self.UNSIGNED_CHAR_FORMAT, self.data[1:2])[0]
        error_code = struct.unpack(self.UNSIGNED_CHAR_FORMAT, self.data[2:3])[0]
        timestamp = struct.unpack(self.DOUBLE_FORMAT, self.data[3:11])[0]
        size_of_body = struct.unpack(self.UNSIGNED_SHORT_FORMAT, self.data[11:13])[0]

        command_id_type = (
            MainCommandId if self.socket == SocketType.MAIN else MoveCommandId
        )

        return Header(
            CommandType(command_type),
            command_id_type(command_id),
            ErrorCode(error_code),
            timestamp,
            size_of_body,
        )

    def decode_struct(self, decode_format: str, size: int, offset: int = 0):
        decoded_data = struct.unpack(
            decode_format,
            self.data[self.HEADER_SIZE + offset : self.HEADER_SIZE + offset + size],
        )
        return decoded_data

    def decode_connect_body(self, size_of_body: int) -> str:
        """
        Decode the text body from the received data.

        Args:
            size_of_body (int): The size of the body to decode.

        Returns:
            str: The decoded text body.
        """
        doubles = struct.unpack(f"{size_of_body}d", self.data[13:])
        characters = [chr(int(d)) for d in doubles]
        return "".join(characters)

    def decode_joint_move_body(self) -> Tuple[float, ...]:
        """
        Decode the body of a joint move message.

        Returns:
            Tuple[float, ...]: 6 floats representing the pose.
        """
        decoded_body = self.decode_struct(
            decode_format=self.POS_FORMAT, size=self.POS_SIZE
        )
        return decoded_body

    def decode_trajectory_move_body(
        self,
    ) -> Tuple[Tuple[float, ...], int, float, float, int]:
        """
        Decode the trajectory move body data.

        Returns:
            Tuple[Tuple[float, ...], int, float, float, int]:
        """

        decoded_pos = self.decode_struct(
            decode_format=self.POS_FORMAT, size=self.POS_SIZE
        )
        decoded_robot_config = self.decode_struct(
            decode_format=self.UNSIGNED_CHAR_FORMAT,
            size=self.ROBOT_CONFIG_SIZE,
            offset=self.POS_SIZE,
        )
        decoded_linear_speed = self.decode_struct(
            decode_format=self.DOUBLE_FORMAT,
            size=self.LINEAR_SPEED_SIZE,
            offset=self.POS_SIZE + self.ROBOT_CONFIG_SIZE,
        )
        decoded_rotation_speed = self.decode_struct(
            decode_format=self.DOUBLE_FORMAT,
            size=self.ROTATION_SPEED_SIZE,
            offset=self.POS_SIZE + self.ROBOT_CONFIG_SIZE + self.LINEAR_SPEED_SIZE,
        )
        decoded_point_id = self.decode_struct(
            decode_format=self.USIGNED_INT,
            size=self.POINT_ID_SIZE,
            offset=self.POS_SIZE
            + self.ROBOT_CONFIG_SIZE
            + self.LINEAR_SPEED_SIZE
            + self.ROTATION_SPEED_SIZE,
        )

        return (
            decoded_pos,
            decoded_robot_config[0],
            decoded_linear_speed[0],
            decoded_rotation_speed[0],
            decoded_point_id[0],
        )

    def decoded_cartesian_move_body(
        self,
    ) -> Tuple[Tuple[float, ...], int, bool]:
        """
        Decode the Cartesian move body data.

        Returns:
            CartesianMove:
                pos (6 floats)
                robot_config (1 int)
                latch_activation (1 bool)
        """
        decoded_pos = self.decode_struct(
            decode_format=self.POS_FORMAT, size=self.POS_SIZE
        )
        decoded_robot_config = self.decode_struct(
            decode_format=self.UNSIGNED_CHAR_FORMAT,
            size=self.ROBOT_CONFIG_SIZE,
            offset=self.POS_SIZE,
        )
        decoded_latch_activation = self.decode_struct(
            decode_format=self.LATCH_ACTIVATION_FORMAT,
            size=self.LATCH_ACTIVATION_SIZE,
            offset=self.POS_SIZE + self.ROBOT_CONFIG_SIZE,
        )

        return decoded_pos, decoded_robot_config[0], decoded_latch_activation[0]

    def decode_body(self, command_id: int, size_of_body: int) -> Command:
        match self.socket, command_id:
            case SocketType.MAIN, 1:
                decoded_body = self.decode_connect_body(size_of_body)
                command = Connect(decoded_body)
            case SocketType.MAIN, 5:
                command = GetState()
            case SocketType.MAIN, 6:
                command = GetLatchPose()
            case SocketType.TRAJECTORY, 1:
                decoded_body = self.decode_joint_move_body()
                command = JointMove(decoded_body)
            case SocketType.TRAJECTORY, 2:
                decoded_body = self.decode_trajectory_move_body()
                command = TrajectoryMove(*decoded_body)
            case SocketType.TRAJECTORY, 5:
                command = InitializeTrajectory()
            case SocketType.TRAJECTORY, 7:
                command = CancelMotion()
            case SocketType.TRAJECTORY, 8:
                decoded_body = self.decoded_cartesian_move_body()
                command = CartesianMove(*decoded_body)

        return command

    def decode(self) -> Command:
        """
        Decode the received data.

        Returns:
            Command
        """
        header = self.decode_header()
        command = self.decode_body(header.command_id, header.size_of_body)
        return command
