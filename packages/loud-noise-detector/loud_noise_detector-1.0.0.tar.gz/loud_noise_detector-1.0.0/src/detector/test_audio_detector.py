import logging
import time
from typing import Any, Callable, Generator, List, cast
from unittest.mock import MagicMock, patch

import pytest

from src.detector.audio_detector import AudioDetector
from src.detector.processors.rms_processor import RMSProcessor
from src.notifiers.base import BaseNotifier
from src.recorders.base import BaseRecorder
from src.utils.config import Config


class MockLogger:
    def __init__(self) -> None:
        self.info = MagicMock()
        self.error = MagicMock()
        self.warning = MagicMock()
        self.debug = MagicMock()
        self.critical = MagicMock()


class TestAudioDetector:
    @pytest.fixture
    def config(self) -> Config:
        config = Config()
        config.threshold = 0.2
        config.cooldown_seconds = 2
        config.chunk_size = 1024
        config.pre_buffer_seconds = 1
        config.rate = 44100
        config.seconds_to_record = 3
        config.verbose = False
        config.logger = cast(logging.Logger, MockLogger())
        return config

    @pytest.fixture
    def recorders(self) -> List[BaseRecorder]:
        recorder = MagicMock(spec=BaseRecorder)
        recorder.save = MagicMock(
            return_value={
                "path": "/tmp/test.wav",
                "temporary": True,
            }
        )
        recorder.remove_file = MagicMock(return_value=True)
        return [cast(BaseRecorder, recorder)]

    @pytest.fixture
    def notifiers(self) -> List[BaseNotifier]:
        notifier = MagicMock(spec=BaseNotifier)
        notifier.notify = MagicMock(return_value=True)
        return [cast(BaseNotifier, notifier)]

    @pytest.fixture
    def detector(
        self,
        config: Config,
        recorders: List[BaseRecorder],
        notifiers: List[BaseNotifier],
    ) -> Generator[AudioDetector, None, None]:
        with patch("pyaudio.PyAudio"):
            with patch("pyaudio.Stream"):
                detector = AudioDetector(config, recorders, notifiers)
                yield detector

    def test_initialization(
        self,
        detector: AudioDetector,
        config: Config,
        recorders: List[BaseRecorder],
        notifiers: List[BaseNotifier],
    ) -> None:
        assert detector.config == config
        assert detector.recorders == recorders
        assert detector.notifiers == notifiers
        assert detector._is_running is False
        assert detector.stream is None
        assert detector.audio is None
        assert isinstance(detector.rms_processor, RMSProcessor)
        assert detector.detection_buffer == []
        assert detector.pre_buffer == []
        assert detector.last_detection_time == 0

    def test_setup(self, detector: AudioDetector) -> None:
        with patch("pyaudio.PyAudio") as mock_pyaudio:
            mock_audio = MagicMock()
            mock_stream = MagicMock()
            mock_audio.open = MagicMock(return_value=mock_stream)
            mock_pyaudio.return_value = mock_audio

            detector.setup()

            assert detector.audio is not None
            assert detector.stream is not None
            assert cast(MagicMock, mock_audio.open).call_count == 1

    def test_cleanup(self, detector: AudioDetector) -> None:
        detector.stream = MagicMock()
        detector.stream.stop_stream = MagicMock()
        detector.stream.close = MagicMock()
        detector.audio = MagicMock()
        detector.audio.terminate = MagicMock()
        detector._is_running = True

        detector.cleanup()

        assert detector._is_running is False
        assert cast(MagicMock, detector.stream.stop_stream).call_count == 1
        assert cast(MagicMock, detector.stream.close).call_count == 1
        assert cast(MagicMock, detector.audio.terminate).call_count == 1

    def test_should_detect_below_threshold(
        self, detector: AudioDetector
    ) -> None:
        result = detector._should_detect(0.1)
        assert result is False

    def test_should_detect_within_cooldown(
        self, detector: AudioDetector
    ) -> None:
        detector.last_detection_time = int(time.time())
        result = detector._should_detect(0.3)
        assert result is False

    def test_should_detect_valid(self, detector: AudioDetector) -> None:
        detector.last_detection_time = int(time.time()) - 3
        result = detector._should_detect(0.3)
        assert result is True

    def test_handle_detection(
        self,
        detector: AudioDetector,
        recorders: List[BaseRecorder],
        notifiers: List[BaseNotifier],
    ) -> None:
        detector.stream = MagicMock()
        detector.stream.read = MagicMock(return_value=b"\x00" * 1024)
        detector.pre_buffer = [b"\x01" * 1024, b"\x02" * 1024]

        detector._handle_detection(0.3, b"\x03" * 1024)

        assert len(detector.detection_buffer) > 0
        assert detector.detection_buffer[0] == b"\x01" * 1024
        assert detector.detection_buffer[1] == b"\x02" * 1024
        assert detector.detection_buffer[2] == b"\x03" * 1024

        assert cast(MagicMock, recorders[0].save).call_count == 1
        assert cast(MagicMock, notifiers[0].notify).call_count == 1

    def test_save_and_notify_keep_files(
        self,
        detector: AudioDetector,
        recorders: List[BaseRecorder],
        notifiers: List[BaseNotifier],
    ) -> None:
        detector.config.keep_files = True
        detector.detection_buffer = [b"\x00" * 1024]

        detector._save_and_notify(0.3, "timestamp")

        assert cast(MagicMock, recorders[0].save).call_count == 1
        assert cast(MagicMock, notifiers[0].notify).call_count == 1
        assert cast(MagicMock, recorders[0].remove_file).call_count == 0

    def test_save_and_notify_delete_files(
        self,
        detector: AudioDetector,
        recorders: List[BaseRecorder],
        notifiers: List[BaseNotifier],
    ) -> None:
        detector.config.keep_files = False
        detector.detection_buffer = [b"\x00" * 1024]

        recorder_save = recorders[0].save
        notifier_notify = notifiers[0].notify
        recorder_remove = recorders[0].remove_file

        detector._save_and_notify(0.3, "timestamp")

        assert cast(MagicMock, recorder_save).call_count == 1
        assert cast(MagicMock, notifier_notify).call_count == 1
        assert cast(MagicMock, recorder_remove).call_count == 1

    def test_stop(self, detector: AudioDetector) -> None:
        detector._is_running = True
        detector.stop()
        assert detector._is_running is False

    def test_start_with_detections(
        self,
        detector: AudioDetector,
        recorders: List[BaseRecorder],
        notifiers: List[BaseNotifier],
    ) -> None:
        with patch.object(detector, "setup") as mock_setup:
            with patch.object(detector, "cleanup") as mock_cleanup:
                mock_stream = MagicMock()
                detector.stream = mock_stream

                read_data = [b"\x00" * 1024, b"\xff" * 1024, b"\x00" * 1024]
                rms_values = [0.1, 0.5, 0.1]

                mock_stream.read = MagicMock(side_effect=read_data)

                rms_patch = patch.object(
                    detector.rms_processor, "calculate", side_effect=rms_values
                )

                with rms_patch:
                    original_handle_detection = detector._handle_detection

                    def make_mock_handle_detection() -> (
                        Callable[[float, bytes], None]
                    ):
                        def mock_handle_detection(
                            rms: float, data: bytes
                        ) -> None:
                            detector._is_running = False
                            original_handle_detection(rms, data)

                        return mock_handle_detection

                    handle_patch = patch.object(
                        detector,
                        "_handle_detection",
                        make_mock_handle_detection(),
                    )

                    with handle_patch:
                        detector.start()

                        mock_setup.assert_called_once()
                        mock_cleanup.assert_called_once()

                        assert len(detector.detection_buffer) > 0
                        assert (
                            cast(MagicMock, recorders[0].save).call_count >= 1
                        )
                        assert (
                            cast(MagicMock, notifiers[0].notify).call_count
                            >= 1
                        )

    def test_start_keyboard_interrupt(self, detector: AudioDetector) -> None:
        with patch.object(detector, "setup") as mock_setup:
            with patch.object(detector, "cleanup") as mock_cleanup:
                mock_stream = MagicMock()
                detector.stream = mock_stream
                mock_stream.read = MagicMock(side_effect=KeyboardInterrupt())

                detector.start()

                mock_setup.assert_called_once()
                mock_cleanup.assert_called_once()

    def test_handle_detection_with_null_stream(
        self,
        detector: AudioDetector,
        recorders: List[BaseRecorder],
    ) -> None:
        detector.stream = None
        detector.pre_buffer = [b"\x01" * 1024]

        detector._handle_detection(0.3, b"\x03" * 1024)

        assert len(detector.detection_buffer) > 0
        assert detector.detection_buffer[0] == b"\x01" * 1024
        assert detector.detection_buffer[1] == b"\x03" * 1024
        for i in range(2, len(detector.detection_buffer)):
            assert detector.detection_buffer[i] == b""

    def test_save_and_notify_notifier_failure(
        self,
        detector: AudioDetector,
        recorders: List[BaseRecorder],
        notifiers: List[BaseNotifier],
    ) -> None:
        detector.detection_buffer = [b"\x00" * 1024]

        cast(MagicMock, notifiers[0].notify).return_value = False

        detector._save_and_notify(0.3, "timestamp")

        assert cast(MagicMock, recorders[0].save).call_count == 1
        assert cast(MagicMock, notifiers[0].notify).call_count == 1

    def test_save_and_notify_recorder_exception(
        self,
        detector: AudioDetector,
        recorders: List[BaseRecorder],
        notifiers: List[BaseNotifier],
    ) -> None:
        detector.detection_buffer = [b"\x00" * 1024]

        cast(MagicMock, recorders[0].save).side_effect = Exception(
            "Recorder failed"
        )

        with pytest.raises(Exception, match="Recorder failed"):
            detector._save_and_notify(0.3, "timestamp")

        assert cast(MagicMock, recorders[0].save).call_count == 1
        assert cast(MagicMock, notifiers[0].notify).call_count == 0

    def test_verbose_mode(
        self,
        detector: AudioDetector,
    ) -> None:
        detector.config.verbose = True

        with patch.object(detector, "setup"):
            with patch.object(detector, "cleanup"):
                mock_stream = MagicMock()
                detector.stream = mock_stream

                def set_running_false(*args: Any, **kwargs: Any) -> bytes:
                    detector._is_running = False
                    return b"\x00" * 1024

                mock_stream.read = MagicMock(side_effect=set_running_false)

                rms_patch = patch.object(
                    detector.rms_processor, "calculate", return_value=0.1
                )

                with rms_patch:
                    with patch("builtins.print") as mock_print:
                        detector.start()

                        assert mock_print.call_count >= 1
