import json

import pytest

from robot_simulator.core.settings_manager import SettingsManager


@pytest.fixture
def mock_settings():
    with open("tests/mocks/mock_settings.json") as json_file:
        return json.load(json_file)


@pytest.fixture
def mock_latency_setting(mock_settings):
    return mock_settings["latency"]


@pytest.fixture
def settings_manager(mock_settings):
    return SettingsManager(mock_settings)


def test__load_default_settings(settings_manager, mock_settings):
    assert settings_manager.settings.latency == 0


def test_update_settings(settings_manager):
    settings_manager.update_settings(
        [
            {
                "type": "settings",
                "key": "latency",
                "value": 2.3,
            }
        ]
    )

    assert settings_manager.settings.latency == 2.3
