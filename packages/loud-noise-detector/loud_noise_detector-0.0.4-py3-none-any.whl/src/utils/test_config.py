import json
import os
import tempfile
from typing import Any, Generator

import pytest
import yaml
from pytest import MonkeyPatch

from src.utils.config import Config


class TestConfig:
    @pytest.fixture
    def temp_yaml_config(self) -> Generator[str, None, None]:
        config_data = {
            "threshold": 0.2,
            "cooldown_seconds": 10,
            "seconds_to_record": 10,
            "keep_files": False,
            "verbose": True,
            "language": "es",
        }

        with tempfile.NamedTemporaryFile(
            suffix=".yaml", delete=False, mode="w"
        ) as temp:
            yaml.dump(config_data, temp)
            temp_path = temp.name

        yield temp_path
        # Cleanup
        os.unlink(temp_path)

    @pytest.fixture
    def temp_json_config(self) -> Generator[str, None, None]:
        config_data = {
            "threshold": 0.3,
            "cooldown_seconds": 15,
            "seconds_to_record": 15,
            "keep_files": True,
            "verbose": False,
            "language": "en",
        }

        with tempfile.NamedTemporaryFile(
            suffix=".json", delete=False, mode="w"
        ) as temp:
            json.dump(config_data, temp)
            temp_path = temp.name

        yield temp_path
        # Cleanup
        os.unlink(temp_path)

    def test_default_config(self) -> None:
        config = Config()

        assert config.threshold == 0.1
        assert config.cooldown_seconds == 5
        assert config.seconds_to_record == 5
        assert config.pre_buffer_seconds == 2
        assert config.rate == 44100
        assert config.channels == 1
        assert config.format == 8
        assert config.chunk_size == 1024
        assert config.keep_files is True
        assert config.verbose is False
        assert config.timestamp_format == "%Y%m%d_%H%M%S"
        assert config.language == "en"
        assert config.notifier_options == {}

    def test_yaml_config_loading(self, temp_yaml_config: str) -> None:
        config = Config(temp_yaml_config)

        assert config.threshold == 0.2
        assert config.cooldown_seconds == 10
        assert config.seconds_to_record == 10
        assert config.keep_files is False
        assert config.verbose is True
        assert config.language == "es"

    def test_json_config_loading(self, temp_json_config: str) -> None:
        config = Config(temp_json_config)

        assert config.threshold == 0.3
        assert config.cooldown_seconds == 15
        assert config.seconds_to_record == 15
        assert config.keep_files is True
        assert config.verbose is False
        assert config.language == "en"

    def test_invalid_config_file(self) -> None:
        # Using a non-existent file should not raise an error,
        # it should just use defaults
        config = Config("non_existent_file.yaml")

        assert config.threshold == 0.1
        assert config.language == "en"

    def test_get_localized_text(self, monkeypatch: MonkeyPatch) -> None:
        # Mock the open function to return a fixed translation
        mock_translations = {"listening": "Escuchando ruidos fuertes..."}

        def mock_open(*args: Any, **kwargs: Any) -> Any:
            class MockFile:
                def __enter__(self) -> Any:
                    return self

                def __exit__(self, *args: Any, **kwargs: Any) -> None:
                    pass

                def read(self) -> str:
                    return json.dumps(mock_translations)

            return MockFile()

        monkeypatch.setattr("builtins.open", mock_open)

        config = Config()
        config.language = "es"

        # Test with known key
        assert (
            config.get_localized_text("listening")
            == "Escuchando ruidos fuertes..."
        )

        # Test with unknown key
        assert config.get_localized_text("unknown_key") == "unknown_key"
