import logging
import os
import tempfile
import wave
from typing import Generator, cast
from unittest.mock import MagicMock

import pytest

from src.recorders.wave_recorder import WaveRecorder
from src.utils.config import Config


class MockLogger:
    def __init__(self) -> None:
        self.info = MagicMock()
        self.error = MagicMock()
        self.warning = MagicMock()
        self.debug = MagicMock()
        self.critical = MagicMock()


class TestWaveRecorder:
    @pytest.fixture
    def temp_dir(self) -> Generator[str, None, None]:
        with tempfile.TemporaryDirectory() as tmpdirname:
            yield tmpdirname

    @pytest.fixture
    def config(self) -> Config:
        config = Config()
        config.channels = 1
        config.rate = 44100
        config.verbose = False
        config.logger = cast(logging.Logger, MockLogger())
        return config

    @pytest.fixture
    def recorder(self, temp_dir: str) -> WaveRecorder:
        return WaveRecorder(
            output_dir=temp_dir, prefix="test_", temporary=True
        )

    def test_init_creates_directory(self, temp_dir: str) -> None:
        # Remove the directory created by the fixture
        os.rmdir(temp_dir)
        assert not os.path.exists(temp_dir)

        # The constructor should create the directory
        WaveRecorder(output_dir=temp_dir)
        assert os.path.exists(temp_dir)

    def test_save(
        self, recorder: WaveRecorder, config: Config, temp_dir: str
    ) -> None:
        chunks = [b"\x00\x00" * 1024, b"\x01\x00" * 1024]
        timestamp = "20230525_123456"
        normalized_rms = 0.5

        result = recorder.save(chunks, config, timestamp, normalized_rms)

        # Check if file exists
        expected_path = os.path.join(temp_dir, f"test_{timestamp}.wav")
        assert os.path.exists(expected_path)

        # Check if file has correct content
        with wave.open(expected_path, "rb") as wf:
            assert wf.getnchannels() == config.channels
            assert wf.getsampwidth() == 2
            assert wf.getframerate() == config.rate
            assert wf.readframes(wf.getnframes()) == b"".join(chunks)

        # Check the returned metadata
        assert result["path"] == expected_path
        assert result["format"] == "wav"
        assert result["temporary"] is True
        assert result["timestamp"] == timestamp
        assert result["rms"] == normalized_rms

    def test_save_verbose(
        self, recorder: WaveRecorder, config: Config, temp_dir: str
    ) -> None:
        config.verbose = True
        chunks = [b"\x00\x00" * 1024]
        timestamp = "20230525_123456"

        recorder.save(chunks, config, timestamp, 0.5)

        assert cast(MagicMock, config.logger.info).call_count == 1

    def test_remove_file(
        self, recorder: WaveRecorder, config: Config, temp_dir: str
    ) -> None:
        # Create a test file
        test_file = os.path.join(temp_dir, "test_file.wav")
        with open(test_file, "wb") as f:
            f.write(b"test")

        assert os.path.exists(test_file)

        # Test file removal
        result = recorder.remove_file(test_file, config)

        assert result is True
        assert not os.path.exists(test_file)

    def test_remove_file_verbose(
        self, recorder: WaveRecorder, config: Config, temp_dir: str
    ) -> None:
        config.verbose = True

        # Create a test file
        test_file = os.path.join(temp_dir, "test_file.wav")
        with open(test_file, "wb") as f:
            f.write(b"test")

        recorder.remove_file(test_file, config)

        assert cast(MagicMock, config.logger.info).call_count == 1

    def test_remove_nonexistent_file(
        self, recorder: WaveRecorder, config: Config
    ) -> None:
        result = recorder.remove_file("/nonexistent/path.wav", config)

        assert result is False
