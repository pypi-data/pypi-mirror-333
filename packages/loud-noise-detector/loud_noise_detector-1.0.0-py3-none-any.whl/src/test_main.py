import os
from typing import Generator
from unittest.mock import MagicMock, patch

import pytest

from src.main import main, parse_arguments


class TestMain:
    @pytest.fixture
    def mock_config(self) -> Generator[MagicMock, None, None]:
        with patch("src.main.Config") as mock_config_class:
            mock_config = MagicMock()
            mock_config.verbose = False
            mock_config.language = "en"
            mock_config.keep_files = True
            mock_config_class.return_value = mock_config
            yield mock_config

    @pytest.fixture
    def mock_logger(self) -> Generator[MagicMock, None, None]:
        with patch("src.main.setup_logger") as mock_setup_logger:
            mock_logger = MagicMock()
            mock_setup_logger.return_value = mock_logger
            yield mock_logger

    @pytest.fixture
    def mock_recorder(self) -> Generator[MagicMock, None, None]:
        with patch("src.main.WaveRecorder") as mock_recorder_class:
            mock_recorder = MagicMock()
            mock_recorder_class.return_value = mock_recorder
            yield mock_recorder

    @pytest.fixture
    def mock_detector(self) -> Generator[MagicMock, None, None]:
        with patch("src.main.AudioDetector") as mock_detector_class:
            mock_detector = MagicMock()
            mock_detector_class.return_value = mock_detector
            yield mock_detector_class

    def test_parse_arguments_default(self) -> None:
        with patch("sys.argv", ["main.py"]):
            args = parse_arguments()
            assert args.config == "config/default_config.yaml"
            assert args.verbose is False
            assert args.output_dir == "data/recordings"
            assert args.threshold is None
            assert args.language == "en"
            assert args.delete_files is False

    def test_parse_arguments_custom(self) -> None:
        test_args = [
            "main.py",
            "--config",
            "custom_config.yaml",
            "--verbose",
            "--output-dir",
            "custom/dir",
            "--threshold",
            "0.3",
            "--language",
            "es",
            "--no-keep-files",
        ]
        with patch("sys.argv", test_args):
            args = parse_arguments()
            assert args.config == "custom_config.yaml"
            assert args.verbose is True
            assert args.output_dir == "custom/dir"
            assert args.threshold == 0.3
            assert args.language == "es"
            assert args.delete_files is True

    def test_main_success(
        self,
        mock_config: MagicMock,
        mock_logger: MagicMock,
        mock_recorder: MagicMock,
        mock_detector: MagicMock,
    ) -> None:
        with patch("sys.argv", ["main.py"]):
            with patch("os.makedirs"):
                with patch.dict(os.environ, {}, clear=True):
                    result = main()

                    assert result == 0
                    mock_detector.assert_called_once()
                    mock_detector.return_value.start.assert_called_once()

    def test_main_keyboard_interrupt(
        self,
        mock_config: MagicMock,
        mock_logger: MagicMock,
        mock_recorder: MagicMock,
        mock_detector: MagicMock,
    ) -> None:
        mock_detector.return_value.start.side_effect = KeyboardInterrupt()

        with patch("sys.argv", ["main.py"]):
            with patch("os.makedirs"):
                result = main()

                assert result == 0
                mock_logger.info.assert_called_once()
                mock_detector.assert_called_once()

    def test_main_exception(
        self,
        mock_config: MagicMock,
        mock_logger: MagicMock,
        mock_recorder: MagicMock,
        mock_detector: MagicMock,
    ) -> None:
        mock_detector.return_value.start.side_effect = Exception("Test error")

        with patch("sys.argv", ["main.py"]):
            with patch("os.makedirs"):
                result = main()

                assert result == 1
                mock_logger.error.assert_called_once()
                mock_detector.assert_called_once()

    def test_main_with_slack_configured(
        self,
        mock_config: MagicMock,
        mock_logger: MagicMock,
        mock_recorder: MagicMock,
        mock_detector: MagicMock,
    ) -> None:
        mock_slack_notifier = MagicMock()

        with patch(
            "src.main.SlackNotifier.create_if_configured",
            return_value=mock_slack_notifier,
        ):
            with patch("sys.argv", ["main.py"]):
                with patch("os.makedirs"):
                    result = main()

                    assert result == 0
                    mock_detector.assert_called_once()
                    call_args = mock_detector.call_args[0]
                    assert call_args[0] == mock_config
                    assert call_args[1] == [mock_recorder]
                    assert call_args[2] == [mock_slack_notifier]
                    mock_detector.return_value.start.assert_called_once()

    def test_main_without_slack_configured(
        self,
        mock_config: MagicMock,
        mock_logger: MagicMock,
        mock_recorder: MagicMock,
        mock_detector: MagicMock,
    ) -> None:
        with patch(
            "src.main.SlackNotifier.create_if_configured", return_value=None
        ):
            with patch("sys.argv", ["main.py"]):
                with patch("os.makedirs"):
                    result = main()

                    assert result == 0
                    mock_detector.assert_called_once()
                    call_args = mock_detector.call_args[0]
                    assert call_args[0] == mock_config
                    assert call_args[1] == [mock_recorder]
                    assert call_args[2] == []
                    mock_detector.return_value.start.assert_called_once()
