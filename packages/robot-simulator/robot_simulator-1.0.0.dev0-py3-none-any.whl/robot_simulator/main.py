import asyncio
from argparse import ArgumentParser

from robot_simulator.core.robot_simulator_server import RobotSimulator


def parse_args():
    parser = ArgumentParser()
    parser.add_argument(
        "--host", type=str, default="localhost", help="Host address of the server"
    )
    parser.add_argument(
        "--framework-port",
        type=int,
        default=12345,
        help="Port number of the server for the test framework",
    )
    parser.add_argument(
        "--main-port",
        type=int,
        default=1001,
        help="Port number of the server for the main commands",
    )
    parser.add_argument(
        "--trajectory-port",
        type=int,
        default=1002,
        help="Port number of the server for the trajectory commands",
    )
    return parser.parse_args()


if __name__ == "__main__":
    robot_simulator = RobotSimulator(**vars(parse_args()))
    asyncio.run(robot_simulator.start())
