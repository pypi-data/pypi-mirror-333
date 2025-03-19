import json
import logging
from unittest.mock import MagicMock

import pytest

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
from robot_simulator.core.encoder import Encoder
from robot_simulator.core.responses import Responses
from robot_simulator.core.responses_manager import ResponsesManager


@pytest.fixture
def mock_timestamp(monkeypatch):
    mock_timestamp = 10.10
    monkeypatch.setattr("robot_simulator.core.commands.time.time", lambda: mock_timestamp)
    return mock_timestamp


@pytest.fixture
def mock_responses():
    with open("tests/mocks/mock_responses.json") as json_file:
        return json.load(json_file)


@pytest.fixture
def mock_connect_response(mock_responses):
    return mock_responses["main"]["1"]["version"]


@pytest.fixture
def mock_responses_object(mock_responses):
    return ResponsesManager(mock_responses).find_responses()


@pytest.fixture
def empty_mock_responses() -> Responses:
    return Responses("", {}, [], [])


def test_socket_type():
    assert SocketType.MAIN.value == 0
    assert SocketType.TRAJECTORY.value == 1


def test_command_type():
    assert CommandType.STANDARD.value == 0


def test_main_command_id():
    assert MainCommandId.CONNECT.value == 1
    assert MainCommandId.HERE.value == 4
    assert MainCommandId.GETSTATE.value == 5
    assert MainCommandId.GETLATCHEDPOSE.value == 6


def test_movement_command_id():
    assert MoveCommandId.JOINTMOVE.value == 1
    assert MoveCommandId.TRAJECTORYMOVE.value == 2
    assert MoveCommandId.INITIALIZETRAJECTORY.value == 5
    assert MoveCommandId.CANCELMOTION.value == 7
    assert MoveCommandId.CARTESIANMOVE.value == 8


def test_error_code():
    assert ErrorCode.SUCCESS.value == 0
    assert ErrorCode.FAILURE.value == 1


def test_command_header():
    header = Header(
        CommandType.STANDARD,
        MainCommandId.CONNECT,
        ErrorCode.SUCCESS,
        0.0,
        0,
    )
    assert header.command_type.value == 0
    assert header.command_id.value == 1
    assert header.error_code.value == 0
    assert header.timestamp == 0.0
    assert header.size_of_body == 0


def test_connect():
    connect = Connect("0.0.0")
    assert connect.body == "0.0.0"


def test_connnect_get_response_return_acknowledgement(
    mock_responses_object, mock_connect_response
):
    connect = Connect(mock_connect_response)
    # Due to double ack for connect request in stabuli firmware
    assert (
        connect.get_response(mock_responses_object)
        == connect.acknowledgement + connect.acknowledgement
    )


def test_connect_get_response_return_response(mock_responses_object, mock_timestamp):
    connect = Connect("2.2.2")
    body = connect.encoder.encode_connect_response(mock_responses_object.connect)
    header = connect.create_header(ErrorCode.VERSION_ERROR, body)
    assert connect.get_response(mock_responses_object) == header + body


def test_trajectorymove_data():
    pos = (0.1, 0.2, 0.3, 0.4, 0.5, 0.6)
    robot_config = 0
    linear_speed = 0.1
    rotation_speed = 0.2
    point_id = 0
    trajectory_move = TrajectoryMove(
        pos, robot_config, linear_speed, rotation_speed, point_id
    )
    assert trajectory_move.body == (
        pos,
        robot_config,
        linear_speed,
        rotation_speed,
        point_id,
    )
    assert trajectory_move.pos == pos
    assert trajectory_move.robot_config == robot_config
    assert trajectory_move.linear_speed == linear_speed
    assert trajectory_move.rotation_speed == rotation_speed
    assert trajectory_move.point_id == point_id


def test_trajectorymove_get_response_return_response(
    mock_timestamp, mock_responses_object, caplog
):
    trajectory_move = TrajectoryMove((0.1, 0.2, 0.3, 0.4, 0.5, 0.6), 0, 0.1, 0.2, 8)
    response = trajectory_move.get_response(mock_responses_object)

    body = Encoder().encode_trajectorymove_response(
        mock_responses_object.trajectorymove
    )
    header = trajectory_move.create_header(ErrorCode.SUCCESS, body)

    caplog.set_level(logging.INFO)
    assert response == header + body


def test_trajectorymove_remove_values_if_none():
    trajectory_move = TrajectoryMove((0.1, 0.2, 0.3, 0.4, 0.5, 0.6), 0, 0.1, 0.2, 8)
    trajectorymove_responses = {
        "cartesian_positions": None,
        "robot_config": None,
        "point_id": None,
    }
    expected_response = {
        "cartesian_positions": (0.1, 0.2, 0.3, 0.4, 0.5, 0.6),
        "robot_config": 0,
        "point_id": 8,
    }
    assert (
        trajectory_move.replace_values_if_none(trajectorymove_responses)
        == expected_response
    )


def test_cartesian_move_data():
    pos = (0.1, 0.2, 0.3, 0.4, 0.5, 0.6)
    robot_config = 0
    latch_activation = True
    cartesian_move_data = CartesianMove(pos, robot_config, latch_activation)
    assert cartesian_move_data.body == (pos, robot_config, latch_activation)
    assert cartesian_move_data.pos == pos
    assert cartesian_move_data.robot_config == robot_config
    assert cartesian_move_data.latch_activation == latch_activation


def test_cartesian_move_get_response_return_acknowledgement(mock_responses_object):
    cartesian_move = CartesianMove((0.1, 0.2, 0.3, 0.4, 0.5, 0.6), 0, True)
    assert (
        cartesian_move.get_response(mock_responses_object)
        == cartesian_move.acknowledgement
    )


def test_command():
    command = Command()
    assert command.body is None


def test_command_get_response():
    mock_responses = MagicMock()
    command = Command()
    assert command.get_response(mock_responses) == b""


def test_getstate():
    get_state = GetState()
    assert get_state.body is None


def test_gatstate_get_response_return_response(mock_responses_object, mock_timestamp):
    get_state = GetState()
    response = get_state.get_response(mock_responses_object)

    body = Encoder().encode_getstate_response(mock_responses_object.getstate)
    header = get_state.create_header(ErrorCode.SUCCESS, body)

    assert response == header + body


def test_gatstate_get_response_return_no_response(empty_mock_responses, caplog):
    get_state = GetState()

    with pytest.raises(SystemExit):
        get_state.get_response(empty_mock_responses)

    assert "No responses for GetState command found" in caplog.text


def test_getlatch_pose():
    get_latch_pose = GetLatchPose()
    assert get_latch_pose.body is None


def test_getlatch_pose_get_response_return_response(
    mock_responses_object, mock_timestamp
):
    get_latch_pose = GetLatchPose()

    body = Encoder().encode_getlatchedpose_response(
        mock_responses_object.getlatchedpose
    )
    header = get_latch_pose.create_header(ErrorCode.SUCCESS, body)
    response = get_latch_pose.get_response(mock_responses_object)

    assert response == header + body


def test_joint_move():
    pos = (0.1, 0.2, 0.3, 0.4, 0.5, 0.6)
    joint_move = JointMove(pos)
    assert joint_move.body == pos


def test_joint_move_get_response_return_acknowledgement(mock_responses_object):
    joint_move = JointMove((0.1, 0.2, 0.3, 0.4, 0.5, 0.6))
    assert joint_move.get_response(mock_responses_object) == joint_move.acknowledgement


def test_initialize_trajectory():
    initialize_trajectory = InitializeTrajectory()
    assert initialize_trajectory.body is None


def test_initialize_trajectory_get_response_return_acknowledgement(
    mock_responses_object,
):
    initialize_trajectory = InitializeTrajectory()
    assert (
        initialize_trajectory.get_response(mock_responses_object)
        == initialize_trajectory.acknowledgement
    )


def test_cancel_motion():
    cancel_motion = CancelMotion()
    assert cancel_motion.body is None


def test_cancel_motion_get_response_return_acknowledgement(mock_responses_object):
    cancel_motion = CancelMotion()
    assert (
        cancel_motion.get_response(mock_responses_object)
        == cancel_motion.acknowledgement
    )
