import array
import math

import pytest

from src.detector.processors.rms_processor import RMSProcessor
from src.utils.config import Config


class TestRMSProcessor:
    @pytest.fixture
    def config(self) -> Config:
        return Config()

    @pytest.fixture
    def processor(self, config: Config) -> RMSProcessor:
        return RMSProcessor(config)

    def test_calculate_normal_data(self, processor: RMSProcessor) -> None:
        # Create sample data with some values
        sample_data = array.array("h", [100, 200, 300, 400]).tobytes()

        # Calculate expected RMS manually
        data_array = array.array("h", sample_data)
        sum_squares = sum(sample * sample for sample in data_array)
        expected_rms = math.sqrt(sum_squares / len(data_array))
        expected_normalized_rms = expected_rms / 32767

        # Test the method
        result = processor.calculate(sample_data)

        assert result == pytest.approx(expected_normalized_rms)

    def test_calculate_zero_data(self, processor: RMSProcessor) -> None:
        # Create sample data with zeros
        sample_data = array.array("h", [0, 0, 0, 0]).tobytes()

        # Test the method
        result = processor.calculate(sample_data)

        assert result == 0

    def test_calculate_empty_data(self, processor: RMSProcessor) -> None:
        # Create empty data
        sample_data = array.array("h", []).tobytes()

        # Test the method
        result = processor.calculate(sample_data)

        assert result == 0
