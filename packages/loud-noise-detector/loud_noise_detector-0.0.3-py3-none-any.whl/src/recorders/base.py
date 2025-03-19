from abc import ABC, abstractmethod
from typing import Any, Dict, List

from src.utils.config import Config


class BaseRecorder(ABC):

    @abstractmethod
    def save(
        self,
        chunks: List[bytes],
        config: Config,
        timestamp: str,
        normalized_rms: float,
    ) -> Dict[str, Any]:
        pass

    @abstractmethod
    def remove_file(self, file_path: str, config: Config) -> bool:
        pass
