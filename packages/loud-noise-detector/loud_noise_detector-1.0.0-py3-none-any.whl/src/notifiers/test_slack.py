import logging
import os
from typing import Any, cast
from unittest.mock import MagicMock, patch

import pytest

from src.notifiers.slack import SlackNotifier
from src.utils.config import Config


class MockLogger:

    def __init__(self) -> None:
        self.info = MagicMock()
        self.error = MagicMock()
        self.warning = MagicMock()
        self.debug = MagicMock()
        self.critical = MagicMock()


class TestSlackNotifier:
    @pytest.fixture
    def config(self) -> Config:
        config = Config()
        config.logger = cast(logging.Logger, MockLogger())
        return config

    @pytest.fixture
    def notifier(self) -> SlackNotifier:
        return SlackNotifier()

    @pytest.fixture
    def recordings(self) -> list[dict[str, Any]]:
        return [{"path": "/tmp/test_recording.wav", "format": "wav"}]

    def test_notify_missing_token(
        self,
        notifier: SlackNotifier,
        config: Config,
        recordings: list[dict[str, Any]],
    ) -> None:
        # Ensure environment variable is not set
        with patch.dict(os.environ, {}, clear=True):
            result = notifier.notify(recordings, "timestamp", 0.5, config)

            assert result is False
            assert cast(MagicMock, config.logger.error).call_count == 1

    def test_notify_missing_channel(
        self,
        notifier: SlackNotifier,
        config: Config,
        recordings: list[dict[str, Any]],
    ) -> None:
        # Set token but no channel
        with patch.dict(os.environ, {"SLACK_TOKEN": "test_token"}, clear=True):
            result = notifier.notify(recordings, "timestamp", 0.5, config)

            assert result is False
            assert cast(MagicMock, config.logger.error).call_count == 1

    def test_notify_no_recordings(
        self, notifier: SlackNotifier, config: Config
    ) -> None:
        # Set both token and channel
        with patch.dict(
            os.environ,
            {"SLACK_TOKEN": "test_token", "SLACK_CHANNEL": "test_channel"},
            clear=True,
        ):
            result = notifier.notify([], "timestamp", 0.5, config)

            assert result is False
            assert cast(MagicMock, config.logger.error).call_count == 1

    def test_notify_successful(
        self,
        notifier: SlackNotifier,
        config: Config,
        recordings: list[dict[str, Any]],
    ) -> None:
        # Mock requests.post
        mock_response = MagicMock()
        mock_response.json.return_value = {"ok": True}

        with patch("requests.post", return_value=mock_response):
            with patch(
                "builtins.open",
                MagicMock(
                    return_value=MagicMock(
                        __enter__=MagicMock(
                            return_value=MagicMock(
                                read=MagicMock(return_value=b"content")
                            )
                        )
                    )
                ),
            ):
                with patch.dict(
                    os.environ,
                    {
                        "SLACK_TOKEN": "test_token",
                        "SLACK_CHANNEL": "test_channel",
                    },
                    clear=True,
                ):
                    result = notifier.notify(
                        recordings, "timestamp", 0.5, config
                    )

                    assert result is True

    def test_notify_api_error(
        self,
        notifier: SlackNotifier,
        config: Config,
        recordings: list[dict[str, Any]],
    ) -> None:
        # Mock requests.post with error response
        mock_response = MagicMock()
        mock_response.json.return_value = {"ok": False, "error": "some_error"}

        with patch("requests.post", return_value=mock_response):
            with patch(
                "builtins.open",
                MagicMock(
                    return_value=MagicMock(
                        __enter__=MagicMock(
                            return_value=MagicMock(
                                read=MagicMock(return_value=b"content")
                            )
                        )
                    )
                ),
            ):
                with patch.dict(
                    os.environ,
                    {
                        "SLACK_TOKEN": "test_token",
                        "SLACK_CHANNEL": "test_channel",
                    },
                    clear=True,
                ):
                    result = notifier.notify(
                        recordings, "timestamp", 0.5, config
                    )

                    assert result is False
                    assert cast(MagicMock, config.logger.error).call_count == 3

    def test_notify_exception(
        self,
        notifier: SlackNotifier,
        config: Config,
        recordings: list[dict[str, Any]],
    ) -> None:
        # Mock requests.post to raise exception
        with patch("requests.post", side_effect=Exception("Test error")):
            with patch(
                "builtins.open",
                MagicMock(
                    return_value=MagicMock(
                        __enter__=MagicMock(
                            return_value=MagicMock(
                                read=MagicMock(return_value=b"content")
                            )
                        )
                    )
                ),
            ):
                with patch.dict(
                    os.environ,
                    {
                        "SLACK_TOKEN": "test_token",
                        "SLACK_CHANNEL": "test_channel",
                    },
                    clear=True,
                ):
                    result = notifier.notify(
                        recordings, "timestamp", 0.5, config
                    )

                    assert result is False
                    assert cast(MagicMock, config.logger.error).call_count == 3

    def test_create_if_configured_with_env_vars(self, config: Config) -> None:
        with patch.dict(
            os.environ,
            {"SLACK_TOKEN": "test_token", "SLACK_CHANNEL": "test_channel"},
            clear=True,
        ):
            notifier = SlackNotifier.create_if_configured(config)
            assert notifier is not None
            assert notifier.token == "test_token"
            assert notifier.channel == "test_channel"

    def test_create_if_configured_with_config(self, config: Config) -> None:
        config.notifier_options = {
            "slack": {"token": "config_token", "channel": "config_channel"}
        }
        notifier = SlackNotifier.create_if_configured(config)
        assert notifier is not None
        assert notifier.token == "config_token"
        assert notifier.channel == "config_channel"

    def test_create_if_configured_with_params(self, config: Config) -> None:
        notifier = SlackNotifier.create_if_configured(
            config, token="param_token", channel="param_channel"
        )
        assert notifier is not None
        assert notifier.token == "param_token"
        assert notifier.channel == "param_channel"

    def test_create_if_configured_missing_token(self, config: Config) -> None:
        with patch.dict(
            os.environ, {"SLACK_CHANNEL": "test_channel"}, clear=True
        ):
            notifier = SlackNotifier.create_if_configured(config)
            assert notifier is None
            assert cast(MagicMock, config.logger.warning).call_count == 1

    def test_create_if_configured_missing_channel(
        self, config: Config
    ) -> None:
        with patch.dict(os.environ, {"SLACK_TOKEN": "test_token"}, clear=True):
            notifier = SlackNotifier.create_if_configured(config)
            assert notifier is None
            assert cast(MagicMock, config.logger.warning).call_count == 1

    def test_create_if_configured_priority(self, config: Config) -> None:
        with patch.dict(
            os.environ,
            {"SLACK_TOKEN": "env_token", "SLACK_CHANNEL": "env_channel"},
            clear=True,
        ):
            config.notifier_options = {
                "slack": {"token": "config_token", "channel": "config_channel"}
            }
            notifier = SlackNotifier.create_if_configured(
                config, token="param_token", channel="param_channel"
            )
            assert notifier is not None
            assert notifier.token == "param_token"
            assert notifier.channel == "param_channel"
