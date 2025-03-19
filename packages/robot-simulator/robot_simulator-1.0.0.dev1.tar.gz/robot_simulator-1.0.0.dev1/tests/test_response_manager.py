import json

import pytest

from robot_simulator.core.commands import MainCommandId, MoveCommandId
from robot_simulator.core.responses_manager import ResponsesManager


@pytest.fixture
def mock_responses():
    with open("tests/mocks/mock_responses.json") as json_file:
        return json.load(json_file)


@pytest.fixture
def mock_connect_response(mock_responses):
    return mock_responses["main"]["1"]["version"]


@pytest.fixture
def mock_getstate_response(mock_responses):
    return mock_responses["main"]["5"]


@pytest.fixture
def mock_getlatchedpose_response(mock_responses):
    return mock_responses["main"]["6"]


@pytest.fixture
def mock_trajectorymove_response(mock_responses):
    return mock_responses["trajectory"]["2"]


@pytest.fixture
def response_manager(mock_responses):
    return ResponsesManager(mock_responses)


def test__get_main_connect(response_manager, mock_connect_response):
    assert response_manager._get_main_connect() == mock_connect_response


def test__get_main_getstate(response_manager, mock_getstate_response):
    assert response_manager._get_main_getstate() == mock_getstate_response


def test__get_main_getlatchedpose(response_manager):
    assert response_manager._get_main_getlatchedpose() == {
        "cartesian_positions": [0.1, 0.2, 0.3, 0.4, 0.5, 0.6],
        "robot_config": 1,
    }


def test__get_trajectory_move(response_manager):
    assert response_manager._get_trajectory_move() == {
        "cartesian_positions": [1.0, 1.0, 1.0, 0.0, 0.0, 60],
        "robot_config": 1,
        "joint_values": [0.1, 0.2, 0.3, 0.4, 0.5, 0.6],
        "pedal_status": 3,
        "state_machine": 1,
        "safety_state": 1,
        "move_id": 0.5,
        "is_settled": True,
        "latch_status": True,
        "point_id": 8,
    }


def test__find_responses(
    response_manager,
    mock_connect_response,
    mock_getstate_response,
    mock_getlatchedpose_response,
    mock_trajectorymove_response,
):
    main_key = response_manager.MAIN_KEY
    trajectory_key = response_manager.TRAJECTORY_KEY

    assert (
        response_manager._find_responses(main_key, MainCommandId.CONNECT)
        == mock_connect_response
    )
    assert (
        response_manager._find_responses(main_key, MainCommandId.GETSTATE)
        == mock_getstate_response
    )
    assert (
        response_manager._find_responses(main_key, MainCommandId.GETLATCHEDPOSE)
        == mock_getlatchedpose_response
    )
    assert (
        response_manager._find_responses(trajectory_key, MoveCommandId.TRAJECTORYMOVE)
        == mock_trajectorymove_response
    )


def test_find_responses(
    response_manager,
    mock_connect_response,
    mock_getstate_response,
    mock_getlatchedpose_response,
    mock_trajectorymove_response,
):
    responses = response_manager.find_responses()

    assert responses.connect == mock_connect_response
    assert responses.getstate == mock_getstate_response
    assert responses.getlatchedpose == mock_getlatchedpose_response
    assert responses.trajectorymove == mock_trajectorymove_response


def test_update_responses(response_manager):
    response_manager.update_responses(
        [
            {
                "type": "main",
                "id": "1",
                "key": "version",
                "value": "0.5.3b",
            },
            {
                "type": "main",
                "id": "5",
                "key": "cartesian_positions",
                "value": [2.0, 2.0, 2.0, 2.0, 2.0, 60],
            },
            {
                "type": "main",
                "id": "6",
                "key": "cartesian_positions",
                "value": 999.0,
                "index": 3,
            },
            {
                "type": "trajectory",
                "id": "2",
                "key": "joint_values",
                "value": [0.1, 0.2, 0.3, 0.4, 0.5, 0.6],
            },
        ]
    )

    assert response_manager.default_responses["main"]["1"]["version"] == "0.5.3b"
    assert response_manager.default_responses["main"]["5"]["cartesian_positions"] == [
        2.0,
        2.0,
        2.0,
        2.0,
        2.0,
        60,
    ]
    assert response_manager.default_responses["main"]["6"]["cartesian_positions"] == [
        0.1,
        0.2,
        0.3,
        999.0,
        0.5,
        0.6,
    ]
    assert response_manager.default_responses["trajectory"]["2"]["joint_values"] == [
        0.1,
        0.2,
        0.3,
        0.4,
        0.5,
        0.6,
    ]


def test_update_responses_index_error(response_manager):
    with pytest.raises(IndexError):
        response_manager.update_responses(
            [
                {
                    "type": "main",
                    "id": "6",
                    "key": "cartesian_positions",
                    "value": 999.0,
                    "index": 9,
                }
            ]
        )
