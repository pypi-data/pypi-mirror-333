from abc import ABC, abstractmethod
from typing import Any, Dict, List

from src.utils.config import Config


class BaseNotifier(ABC):

    @abstractmethod
    def notify(
        self,
        recordings: List[Dict[str, Any]],
        timestamp: str,
        normalized_rms: float,
        config: Config,
    ) -> bool:
        pass
