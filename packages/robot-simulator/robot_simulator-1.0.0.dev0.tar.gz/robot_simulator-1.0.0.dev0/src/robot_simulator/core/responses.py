from typing import Dict


class Responses:
    def __init__(
        self,
        connect: str,
        getstate: Dict,
        getlatchedpose: Dict,
        trajectorymove: Dict,
    ):
        self.connect = connect
        self.getstate = getstate
        self.getlatchedpose = getlatchedpose
        self.trajectorymove = trajectorymove


default_responses = {
    "main": {
        "1": {"version": "0.5.3a"},
        "5": {
            "cartesian_positions": [1.0, 1.0, 1.0, 0.0, 0.0, 60],
            "robot_config": 1,
            "joint_values": [0.1, 0.2, 0.3, 0.4, 0.5, 0.6],
            "pedal_status": 3,
            "state_machine": 1,
            "safety_state": 0,
            "move_id": 1,
            "is_settled": True,
            "latch_status": False,
        },
        "6": {
            "cartesian_positions": [1.0, 1.0, 1.0, 0.0, 0.0, 60],
            "robot_config": 1,
        },
    },
    "trajectory": {
        "2": {
            "cartesian_positions": None,
            "robot_config": None,
            "joint_values": [0.1, 0.2, 0.3, 0.4, 0.5, 0.6],
            "pedal_status": 3,
            "state_machine": 1,
            "safety_state": 1,
            "move_id": 0.5,
            "is_settled": True,
            "latch_status": True,
            "point_id": None,
        }
    },
}
