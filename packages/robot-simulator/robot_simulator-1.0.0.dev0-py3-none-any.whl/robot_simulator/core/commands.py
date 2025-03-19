import sys
import time
from enum import IntEnum
from typing import Dict, Tuple, Union

from robot_simulator.core.encoder import Encoder
from robot_simulator.core.logger_manager import Logger
from robot_simulator.core.responses import Responses


class SocketType(IntEnum):
    MAIN = 0
    TRAJECTORY = 1
    FRAMEWORK = 2


class CommandType(IntEnum):  # Corresponds to MsgType
    STANDARD = 0


class MainCommandId(IntEnum):
    CONNECT = 1
    HERE = 4
    GETSTATE = 5
    GETLATCHEDPOSE = 6


class MoveCommandId(IntEnum):
    JOINTMOVE = 1
    TRAJECTORYMOVE = 2
    INITIALIZETRAJECTORY = 5
    CANCELMOTION = 7
    CARTESIANMOVE = 8


class ErrorCode(IntEnum):
    SUCCESS = 0
    FAILURE = 1
    VERSION_ERROR = 2


class Header:
    def __init__(
        self,
        command_type: CommandType,
        command_id: MainCommandId,
        error_code: ErrorCode,
        timestamp: float,
        size_of_body: int,
    ):
        self.command_type = command_type
        self.command_id = command_id
        self.error_code = error_code
        self.timestamp = timestamp
        self.size_of_body = size_of_body


class Command:
    def __init__(self, body=None):
        self.body = body
        self.encoder = Encoder()
        self.logger = Logger()
        self.command_type = CommandType.STANDARD
        self.command_id: Union[MainCommandId, MoveCommandId] = None

    def get_response(self, responses: Responses) -> bytes:
        self.logger.log_info(f"{str(self)}.get_response() called")
        return b""

    def create_header(
        self,
        error_code: ErrorCode,
        body: bytes,
    ) -> bytes:
        return self.encoder.encode_header(
            Header(
                command_type=self.command_type,
                command_id=self.command_id,
                error_code=error_code,
                timestamp=time.time(),
                size_of_body=len(body),
            )
        )

    def __str__(self):
        return f"{self.__class__.__name__}"


class Connect(Command):
    def __init__(self, body: str):
        super().__init__(body)
        self.command_id = MainCommandId.CONNECT
        self.acknowledgement = b"\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"

    def get_response(self, responses: Responses) -> bytes:
        if self.body != responses.connect:
            self.logger.log_error(
                f"{self.body} received from client, expected version {responses.connect}"
            )
            encoded_body = self.encoder.encode_connect_response(responses.connect)
            header = self.create_header(
                ErrorCode.VERSION_ERROR,
                encoded_body,
            )
            return header + encoded_body
        else:
            self.logger.log_info("Matching version, sending ack to client")
            # Sending double ack until staubli firmaware is fixed by removing the double ack
            return self.acknowledgement + self.acknowledgement


class GetState(Command):
    def __init__(self):
        super().__init__()
        self.command_id = MainCommandId.GETSTATE

    def get_response(self, responses: Responses) -> bytes:
        if len(responses.getstate) > 0:
            getstate_response = responses.getstate
            self.logger.log_info(f"Response for GetState command: {getstate_response}")
            body = self.encoder.encode_getstate_response(getstate_response)
            header = self.create_header(
                ErrorCode.SUCCESS,
                body,
            )
            return header + body
        else:
            self.logger.log_error("No responses for GetState command found")
            sys.exit(1)


class GetLatchPose(Command):
    def __init__(self):
        super().__init__()
        self.command_id = MainCommandId.GETLATCHEDPOSE

    def get_response(self, responses: Responses) -> bytes:
        self.logger.log_info(
            f"Response for GetLatchPose command: {responses.getlatchedpose}"
        )
        body = self.encoder.encode_getlatchedpose_response(responses.getlatchedpose)
        header = self.create_header(
            ErrorCode.SUCCESS,
            body,
        )
        return header + body


class JointMove(Command):
    def __init__(self, body: Tuple[float, ...]):
        super().__init__()
        self.body = body
        self.acknowledgement = b"\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"

    def get_response(self, responses: Responses) -> bytes:
        return self.acknowledgement


class TrajectoryMove(Command):
    def __init__(
        self,
        pos: Tuple[float, ...],
        robot_config: int,
        linear_speed: float,
        rotation_speed: float,
        point_id: int,
    ):
        super().__init__()
        self.logger.log_info(
            f"TrajectoryMove command initialized with pos: {pos}, robot_config: {robot_config},"
            f" linear_speed: {linear_speed}, rotation_speed: {rotation_speed}, point_id: {point_id}"
        )
        self.command_id = MoveCommandId.TRAJECTORYMOVE
        self.body = (
            pos,
            robot_config,
            linear_speed,
            rotation_speed,
            point_id,
        )
        self.pos = pos
        self.robot_config = robot_config
        self.linear_speed = linear_speed
        self.rotation_speed = rotation_speed
        self.point_id = point_id

    def replace_values_if_none(self, trajectorymove_response: Dict) -> Dict:
        if trajectorymove_response.get("cartesian_positions") is None:
            trajectorymove_response["cartesian_positions"] = self.pos
        if trajectorymove_response.get("robot_config") is None:
            trajectorymove_response["robot_config"] = self.robot_config
        if trajectorymove_response.get("point_id") is None:
            trajectorymove_response["point_id"] = self.point_id
        return trajectorymove_response

    def get_response(self, responses: Responses) -> bytes:
        trajectorymove_response = self.replace_values_if_none(
            responses.trajectorymove.copy()
        )
        self.logger.log_info(
            f"Response for TrajectoryMove command: {trajectorymove_response}"
        )
        body = self.encoder.encode_trajectorymove_response(trajectorymove_response)
        header = self.create_header(
            ErrorCode.SUCCESS,
            body,
        )
        return header + body


class InitializeTrajectory(Command):
    def __init__(self):
        super().__init__()
        self.acknowledgement = b"\x00\x05\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"

    def get_response(self, responses: Responses) -> None:
        self.logger.log_info(
            f"Response for InitializeTrajectory command : Acknowledgement {self.acknowledgement}"
        )
        return self.acknowledgement


class CancelMotion(Command):
    def __init__(self):
        super().__init__()
        self.acknowledgement = b"\x00\x07\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"

    def get_response(self, responses: Responses) -> None:
        self.logger.log_info(
            f"Response for CancelMotion command : Acknowledgement {self.acknowledgement}"
        )
        return self.acknowledgement


class CartesianMove(Command):
    def __init__(
        self, pos: Tuple[float, ...], robot_config: int, latch_activation: bool
    ):
        super().__init__()
        self.body = (pos, robot_config, latch_activation)
        self.pos = pos
        self.robot_config = robot_config
        self.latch_activation = latch_activation
        self.acknowledgement = b"\x00\x08\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"

    def get_response(self, responses: Responses) -> bytes:
        self.logger.log_info(
            f"Response for CartesianMove command : Acknowledgement {self.acknowledgement}"
        )
        return self.acknowledgement
