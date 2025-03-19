import struct

import pytest

from robot_simulator.core.commands import (
    CancelMotion,
    CartesianMove,
    CommandType,
    Connect,
    ErrorCode,
    GetLatchPose,
    GetState,
    InitializeTrajectory,
    JointMove,
    MainCommandId,
    MoveCommandId,
    SocketType,
    TrajectoryMove,
)
from robot_simulator.core.constants import (
    DOUBLE_FORMAT,
    UNSIGNED_CHAR_FORMAT,
    UNSIGNED_SHORT_FORMAT,
    USIGNED_INT,
)
from robot_simulator.core.decoder import DecodeCommand


@pytest.fixture
def main_socket() -> SocketType:
    return SocketType.MAIN


@pytest.fixture
def trajectory_socket() -> SocketType:
    return SocketType.TRAJECTORY


@pytest.fixture
def mock_timestamp(monkeypatch):
    mock_timestamp = 0
    monkeypatch.setattr("core.commands.time.time", lambda: mock_timestamp)
    return mock_timestamp


@pytest.fixture
def encoded_get_state_command() -> bytes:
    header_command_type = struct.pack(UNSIGNED_CHAR_FORMAT, CommandType.STANDARD)
    header_command_id = struct.pack(UNSIGNED_CHAR_FORMAT, MainCommandId.GETSTATE)
    header_error_code = struct.pack(UNSIGNED_CHAR_FORMAT, ErrorCode.SUCCESS)
    header_timestamp = struct.pack(DOUBLE_FORMAT, 0)
    header_size_of_body = struct.pack(UNSIGNED_SHORT_FORMAT, 0)
    return (
        header_command_type
        + header_command_id
        + header_error_code
        + header_timestamp
        + header_size_of_body
    )


@pytest.fixture
def encoded_get_latch_pose_command() -> bytes:
    header_command_type = struct.pack(UNSIGNED_CHAR_FORMAT, CommandType.STANDARD)
    header_command_id = struct.pack(UNSIGNED_CHAR_FORMAT, MainCommandId.GETLATCHEDPOSE)
    header_error_code = struct.pack(UNSIGNED_CHAR_FORMAT, ErrorCode.SUCCESS)
    header_timestamp = struct.pack(DOUBLE_FORMAT, 0)
    header_size_of_body = struct.pack(UNSIGNED_SHORT_FORMAT, 0)
    return (
        header_command_type
        + header_command_id
        + header_error_code
        + header_timestamp
        + header_size_of_body
    )


@pytest.fixture
def initialize_trajectory_command():
    header_command_type = struct.pack(UNSIGNED_CHAR_FORMAT, CommandType.STANDARD)
    header_command_id = struct.pack(
        UNSIGNED_CHAR_FORMAT, MoveCommandId.INITIALIZETRAJECTORY
    )
    header_error_code = struct.pack(UNSIGNED_CHAR_FORMAT, ErrorCode.SUCCESS)
    header_timestamp = struct.pack(DOUBLE_FORMAT, 0)
    header_size_of_body = struct.pack(UNSIGNED_SHORT_FORMAT, 0)
    return (
        header_command_type
        + header_command_id
        + header_error_code
        + header_timestamp
        + header_size_of_body
    )


@pytest.fixture
def cancel_motion_command():
    header_command_type = struct.pack(UNSIGNED_CHAR_FORMAT, CommandType.STANDARD)
    header_command_id = struct.pack(UNSIGNED_CHAR_FORMAT, MoveCommandId.CANCELMOTION)
    header_error_code = struct.pack(UNSIGNED_CHAR_FORMAT, ErrorCode.SUCCESS)
    header_timestamp = struct.pack(DOUBLE_FORMAT, 0)
    header_size_of_body = struct.pack(UNSIGNED_SHORT_FORMAT, 0)
    return (
        header_command_type
        + header_command_id
        + header_error_code
        + header_timestamp
        + header_size_of_body
    )


@pytest.fixture
def connect_command():
    version = "1.0.0"
    body = struct.pack(f"{len(version)}d", *version.encode())

    header_command_type = struct.pack(UNSIGNED_CHAR_FORMAT, CommandType.STANDARD)
    header_command_id = struct.pack(UNSIGNED_CHAR_FORMAT, MainCommandId.CONNECT)
    header_error_code = struct.pack(UNSIGNED_CHAR_FORMAT, ErrorCode.SUCCESS)
    header_timestamp = struct.pack(DOUBLE_FORMAT, 0)
    header_size_of_body = struct.pack(UNSIGNED_SHORT_FORMAT, len(version))
    header = (
        header_command_type
        + header_command_id
        + header_error_code
        + header_timestamp
        + header_size_of_body
    )
    return header + body


@pytest.fixture
def joint_move_command():
    pose = (1.0, 1.0, 1.0, 0.0, 0.0, 60)
    body = struct.pack(f"{len(pose)}d", *pose)

    header_command_type = struct.pack(UNSIGNED_CHAR_FORMAT, CommandType.STANDARD)
    header_command_id = struct.pack(UNSIGNED_CHAR_FORMAT, MoveCommandId.JOINTMOVE)
    header_error_code = struct.pack(UNSIGNED_CHAR_FORMAT, ErrorCode.SUCCESS)
    header_timestamp = struct.pack(DOUBLE_FORMAT, 0)
    header_size_of_body = struct.pack(UNSIGNED_SHORT_FORMAT, len(pose))
    header = (
        header_command_type
        + header_command_id
        + header_error_code
        + header_timestamp
        + header_size_of_body
    )
    return header + body


@pytest.fixture
def trajectory_move_command():
    pose = (1.0, 1.0, 1.0, 0.0, 0.0, 60)
    robot_config = 1
    linear_speed = 1.1
    rotation_speed = 1.2
    point_id = 8

    encoded_pose = struct.pack(f"{len(pose)}d", *pose)
    encoded_robot_config = struct.pack(UNSIGNED_CHAR_FORMAT, robot_config)
    encoded_linear_speed = struct.pack(DOUBLE_FORMAT, linear_speed)
    encoded_rotation_speed = struct.pack(DOUBLE_FORMAT, rotation_speed)
    encoded_point_id = struct.pack(USIGNED_INT, point_id)

    body = (
        encoded_pose
        + encoded_robot_config
        + encoded_linear_speed
        + encoded_rotation_speed
        + encoded_point_id
    )

    header_command_type = struct.pack(UNSIGNED_CHAR_FORMAT, CommandType.STANDARD)
    header_command_id = struct.pack(UNSIGNED_CHAR_FORMAT, MoveCommandId.TRAJECTORYMOVE)
    header_error_code = struct.pack(UNSIGNED_CHAR_FORMAT, ErrorCode.SUCCESS)
    header_timestamp = struct.pack(DOUBLE_FORMAT, 0)
    header_size_of_body = struct.pack(UNSIGNED_SHORT_FORMAT, len(pose))
    header = (
        header_command_type
        + header_command_id
        + header_error_code
        + header_timestamp
        + header_size_of_body
    )
    return header + body


@pytest.fixture
def cartesian_move_command():
    pos = (1.0, 1.0, 1.0, 0.0, 0.0, 60)
    robot_config = 1
    latch_activation = True

    encoded_pos = struct.pack(f"{len(pos)}d", *pos)
    encoded_robot_config = struct.pack(UNSIGNED_CHAR_FORMAT, robot_config)
    encoded_latch_activation = struct.pack(UNSIGNED_CHAR_FORMAT, latch_activation)

    body = encoded_pos + encoded_robot_config + encoded_latch_activation

    header_command_type = struct.pack(UNSIGNED_CHAR_FORMAT, CommandType.STANDARD)
    header_command_id = struct.pack(UNSIGNED_CHAR_FORMAT, MoveCommandId.CARTESIANMOVE)
    header_error_code = struct.pack(UNSIGNED_CHAR_FORMAT, ErrorCode.SUCCESS)
    header_timestamp = struct.pack(DOUBLE_FORMAT, 0)
    header_size_of_body = struct.pack(UNSIGNED_SHORT_FORMAT, len(pos))
    header = (
        header_command_type
        + header_command_id
        + header_error_code
        + header_timestamp
        + header_size_of_body
    )
    return header + body


def test_get_connect_command(connect_command, main_socket):
    decoder = DecodeCommand(connect_command, main_socket)
    connect_command = decoder.decode()
    assert isinstance(connect_command, Connect)
    assert connect_command.body == "1.0.0"


def test_get_state_command(encoded_get_state_command, main_socket):
    decoder = DecodeCommand(encoded_get_state_command, main_socket)
    get_state_command = decoder.decode()
    assert isinstance(get_state_command, GetState)
    assert get_state_command.body is None


def test_get_latch_pose_command(encoded_get_latch_pose_command, main_socket):
    decoder = DecodeCommand(encoded_get_latch_pose_command, main_socket)
    get_latch_pose_command = decoder.decode()
    assert isinstance(get_latch_pose_command, GetLatchPose)
    assert get_latch_pose_command.body is None


def test_decode_initialize_trajectory_command(
    initialize_trajectory_command, trajectory_socket
):
    decoder = DecodeCommand(initialize_trajectory_command, trajectory_socket)
    command = decoder.decode()
    assert isinstance(command, InitializeTrajectory)
    assert command.body is None


def test_decode_cancel_motion_command(cancel_motion_command, trajectory_socket):
    decoder = DecodeCommand(cancel_motion_command, trajectory_socket)
    command = decoder.decode()
    assert isinstance(command, CancelMotion)
    assert command.body is None


def test_joint_move_command(joint_move_command, trajectory_socket):
    decoder = DecodeCommand(joint_move_command, trajectory_socket)
    command = decoder.decode()
    assert command.body == (1.0, 1.0, 1.0, 0.0, 0.0, 60)
    assert isinstance(command, JointMove)


def test_trajectory_move_command(trajectory_move_command, trajectory_socket):
    decoder = DecodeCommand(trajectory_move_command, trajectory_socket)
    command = decoder.decode()
    assert command.body == ((1.0, 1.0, 1.0, 0.0, 0.0, 60), 1, 1.1, 1.2, 8)
    assert isinstance(command, TrajectoryMove)


def test_decode_cartesian_move_command(cartesian_move_command, trajectory_socket):
    decoder = DecodeCommand(cartesian_move_command, trajectory_socket)
    command = decoder.decode()
    assert command.body == ((1.0, 1.0, 1.0, 0.0, 0.0, 60), 1, True)
    assert isinstance(command, CartesianMove)
