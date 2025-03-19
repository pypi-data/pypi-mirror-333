import struct

import pytest

from robot_simulator.core.constants import DOUBLE_FORMAT, UNSIGNED_CHAR_FORMAT, USIGNED_INT
from robot_simulator.core.encoder import Encoder


@pytest.fixture
def encoder():
    return Encoder()


@pytest.fixture
def cartesian_pos():
    return [1.0, 2.0, 3.0, 4.0, 5.0, 6.0]


@pytest.fixture
def encoded_cartesian_pos(cartesian_pos):
    return struct.pack(f"{len(cartesian_pos)}d", *cartesian_pos)


@pytest.fixture
def robot_config():
    return 1


@pytest.fixture
def encoded_robot_config(robot_config):
    return struct.pack(UNSIGNED_CHAR_FORMAT, robot_config)


@pytest.fixture
def joint_values():
    return [7.0, 8.0, 9.0, 10.0, 11.0, 12.0]


@pytest.fixture
def encoded_joint_values(joint_values):
    return struct.pack(f"{len(joint_values)}d", *joint_values)


@pytest.fixture
def encoded_pedal_status():
    return b"\x03"


@pytest.fixture
def state_machine():
    return 1


@pytest.fixture
def encoded_state_machine(state_machine):
    return struct.pack(UNSIGNED_CHAR_FORMAT, state_machine)


@pytest.fixture
def safety_state():
    return 1


@pytest.fixture
def encoded_safety_state(safety_state):
    return struct.pack(UNSIGNED_CHAR_FORMAT, safety_state)


@pytest.fixture
def move_id():
    return 1.0


@pytest.fixture
def encoded_move_id(move_id):
    return struct.pack(DOUBLE_FORMAT, move_id)


@pytest.fixture
def encoded_is_settled_and_latch_status():
    return b"\x01"


@pytest.fixture
def point_id():
    return 1


@pytest.fixture
def encoded_point_id(point_id):
    return struct.pack(USIGNED_INT, point_id)


def test_encode_pos(encoder, cartesian_pos, encoded_cartesian_pos):
    encoded_pos = encoder.encode_pos(cartesian_pos)
    assert encoded_pos == encoded_cartesian_pos


def test_encode_connect_responses(encoder):
    expected_response = (
        b"\x00\x00\x00\x00\x00\x00H@\x00\x00"
        b"\x00\x00\x00\x00G@\x00\x00\x00\x00\x00"
        b"\x80J@\x00\x00\x00\x00\x00\x00G@\x00\x00"
        b"\x00\x00\x00\x80I@\x00\x00\x00\x00\x00@X@"
    )

    responses = "0.5.3a"
    encoded_responses = encoder.encode_connect_response(responses)

    assert encoded_responses == expected_response


def test_encode_getstate_responses(
    encoder,
    encoded_cartesian_pos,
    encoded_robot_config,
    encoded_joint_values,
    encoded_pedal_status,
    encoded_state_machine,
    encoded_safety_state,
    encoded_move_id,
    encoded_is_settled_and_latch_status,
):
    expected_response = (
        encoded_cartesian_pos
        + encoded_robot_config
        + encoded_joint_values
        + encoded_pedal_status
        + encoded_state_machine
        + encoded_safety_state
        + encoded_move_id
        + encoded_is_settled_and_latch_status
    )

    response = {
        "cartesian_positions": [1.0, 2.0, 3.0, 4.0, 5.0, 6.0],
        "robot_config": 1,
        "joint_values": [7.0, 8.0, 9.0, 10.0, 11.0, 12.0],
        "pedal_status": 3,
        "state_machine": 1,
        "safety_state": 1,
        "move_id": 1.0,
        "is_settled": True,
        "latch_status": False,
    }

    assert encoder.encode_getstate_response(response) == expected_response


def test_encode_getlatchedpose_responses(
    encoder, encoded_cartesian_pos, encoded_robot_config
):
    expected_response = encoded_cartesian_pos + encoded_robot_config

    response = {
        "cartesian_positions": [1.0, 2.0, 3.0, 4.0, 5.0, 6.0],
        "robot_config": 1,
    }

    assert encoder.encode_getlatchedpose_response(response) == expected_response


def test_encode_trajectorymove_responses(
    encoder,
    encoded_cartesian_pos,
    encoded_robot_config,
    encoded_joint_values,
    encoded_pedal_status,
    encoded_state_machine,
    encoded_safety_state,
    encoded_move_id,
    encoded_is_settled_and_latch_status,
    encoded_point_id,
):
    expected_response = (
        encoded_cartesian_pos
        + encoded_robot_config
        + encoded_joint_values
        + encoded_pedal_status
        + encoded_state_machine
        + encoded_safety_state
        + encoded_move_id
        + encoded_is_settled_and_latch_status
        + encoded_point_id
    )

    response = {
        "cartesian_positions": [1.0, 2.0, 3.0, 4.0, 5.0, 6.0],
        "robot_config": 1,
        "point_id": 1,
        "joint_values": [7.0, 8.0, 9.0, 10.0, 11.0, 12.0],
        "pedal_status": 3,
        "state_machine": 1,
        "safety_state": 1,
        "move_id": 1.0,
        "is_settled": True,
        "latch_status": False,
        "point_id": 1,
    }
    assert encoder.encode_trajectorymove_response(response) == expected_response


def test_double_bool_to_bytes(encoder):
    expected_double_true_response = b"\x03"
    assert encoder.double_bool_to_bytes(True, True) == expected_double_true_response

    expected_double_false_response = b"\x00"
    assert encoder.double_bool_to_bytes(False, False) == expected_double_false_response

    expected_true_false_response = b"\x01"
    assert encoder.double_bool_to_bytes(True, False) == expected_true_false_response

    expected_false_true_response = b"\x02"
    assert encoder.double_bool_to_bytes(False, True) == expected_false_true_response
