import asyncio
import json

from robot_simulator.core.commands import SocketType
from robot_simulator.core.decoder import DecodeCommand
from robot_simulator.core.logger_manager import Logger
from robot_simulator.core.responses import default_responses
from robot_simulator.core.responses_manager import ResponsesManager
from robot_simulator.core.settings import default_settings
from robot_simulator.core.settings_manager import SettingsManager


class RobotSimulator:
    def __init__(
        self, host: str, framework_port: int, main_port: int, trajectory_port: int
    ):
        self.host = host
        self.framework_port = framework_port
        self.main_port = main_port
        self.trajectory_port = trajectory_port
        self.logger = Logger()
        self.running = True
        self.responses_manager = ResponsesManager(default_responses)
        self.command_responses = self.responses_manager.find_responses()
        self.settings_manager = SettingsManager(default_settings)

    async def handle_framework(self, reader, writer):
        try:
            while self.running:
                data = await reader.read(10240)
                if not data:
                    break

                json_data = json.loads(data.decode())
                updates = json_data["data"]
                self.logger.log_info(f"Received data from Framework socket: {updates}")

                responses_updates = []
                settings_updates = []
                for update in updates:
                    if update.get("type") == SettingsManager.SETTINGS_KEY:
                        settings_updates.append(update)
                    else:
                        responses_updates.append(update)

                self.responses_manager.update_responses(responses_updates)
                self.settings_manager.update_settings(settings_updates)

        except json.decoder.JSONDecodeError as e:
            response = f"Error decoding JSON: {e}"
            self.logger.log_error(response)

    async def handle_main_commands(self, reader, writer):
        try:
            while self.running:
                data = await reader.read(1024)
                if not data:
                    break

                if self.command_responses:
                    command = DecodeCommand(data, SocketType.MAIN).decode()

                    self.logger.log_info(f"Received data: {data}")
                    self.logger.log_info(
                        f"Received command: {command}, body: {command.body}"
                    )
                    response = command.get_response(self.command_responses)

                    # Simulate latency according to the settings
                    await asyncio.sleep(self.settings_manager.settings.latency)

                    writer.write(response)
                    await writer.drain()
                else:
                    self.logger.log_error("No command responses found")
                    await self.stop()
        except Exception as e:
            self.logger.log_error(f"Error: {e}")
            await self.stop()

    async def handle_trajectory_commands(self, reader, writer):
        try:
            while self.running:
                data = await reader.read(1024)
                if not data:
                    break

                if self.command_responses:
                    command = DecodeCommand(data, SocketType.TRAJECTORY).decode()

                    self.logger.log_info(f"Received data: {data}")
                    self.logger.log_info(
                        f"Received command: {command} body: {command.body}"
                    )
                    response = command.get_response(self.command_responses)

                    # Simulate latency according to the settings
                    await asyncio.sleep(self.settings_manager.settings.latency)

                    writer.write(response)
                    await writer.drain()
                else:
                    self.logger.log_error("No command responses found")
                    await self.stop()
        except Exception as e:
            self.logger.log_error(f"Error: {e}")
            await self.stop()

    async def start(self):
        try:
            framework_server = await asyncio.start_server(
                self.handle_framework, self.host, self.framework_port
            )
            self.logger.log_info(
                f"Framework server started at {self.host}:{self.framework_port}"
            )

            main_server = await asyncio.start_server(
                self.handle_main_commands, self.host, self.main_port
            )
            self.logger.log_info(f"Main server started at {self.host}:{self.main_port}")
            trajectory_server = await asyncio.start_server(
                self.handle_trajectory_commands, self.host, self.trajectory_port
            )
            self.logger.log_info(
                f"Trajectory server started at {self.host}:{self.trajectory_port}"
            )

            framework_server_task = asyncio.create_task(
                framework_server.serve_forever()
            )
            main_server_task = asyncio.create_task(main_server.serve_forever())
            trajectory_server_task = asyncio.create_task(
                trajectory_server.serve_forever()
            )

            await asyncio.gather(
                framework_server_task, main_server_task, trajectory_server_task
            )
        except Exception as e:
            self.logger.log_error(f"Error: {e}")
            await self.stop()

    async def stop(self):
        self.running = False
        await asyncio.sleep(0.1)
