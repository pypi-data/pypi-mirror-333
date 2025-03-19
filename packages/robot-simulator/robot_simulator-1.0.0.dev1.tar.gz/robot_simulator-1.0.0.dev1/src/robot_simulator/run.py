import asyncio
from argparse import ArgumentParser

import typer

from robot_simulator.core.robot_simulator_server import RobotSimulator
from robot_simulator.__init__ import __version__


cli = typer.Typer()


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


def version_callback(value: bool):
    if value:
        typer.echo(__version__)
        raise typer.Exit()


@cli.callback(invoke_without_command=True)
def main(
    ctx: typer.Context,
    version: bool = typer.Option(
        None, "--version", callback=version_callback, is_eager=True
    ),
):
    if ctx.invoked_subcommand is None:
        run_robot_simulator()


@cli.command()
def run_robot_simulator():
    robot_simulator = RobotSimulator(**vars(parse_args()))
    asyncio.run(robot_simulator.start())
