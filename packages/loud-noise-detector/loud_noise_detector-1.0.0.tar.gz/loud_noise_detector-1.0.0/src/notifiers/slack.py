import os
from typing import Any, Dict, List, Optional

import requests

from src.utils.config import Config

from .base import BaseNotifier


class SlackNotifier(BaseNotifier):

    @classmethod
    def create_if_configured(
        cls, config: Config, **kwargs: Any
    ) -> Optional["SlackNotifier"]:
        slack_config = config.notifier_options.get("slack", {})
        token = (
            kwargs.get("token")
            or slack_config.get("token")
            or os.getenv("SLACK_TOKEN")
        )
        channel = (
            kwargs.get("channel")
            or slack_config.get("channel")
            or os.getenv("SLACK_CHANNEL")
        )

        if not token or not channel:
            config.logger.warning(
                "Slack configuration not found."
                " Slack notifications will be disabled."
            )
            return None

        return cls(token=token, channel=channel)

    def __init__(
        self, token: Optional[str] = None, channel: Optional[str] = None
    ):
        self.token = token
        self.channel = channel

    def notify(
        self,
        recordings: List[Dict[str, Any]],
        timestamp: str,
        normalized_rms: float,
        config: Config,
    ) -> bool:
        recording_path = None
        for recording in recordings:
            if "path" in recording:
                recording_path = recording["path"]
                break

        if not recording_path:
            config.logger.error("No recordings available to send to Slack.")
            return False

        message = (
            f"@channel {config.get_localized_text('noise_detected')} "
            f"{timestamp}. "
            f"{config.get_localized_text('rms_amplitude')}: "
            f"{normalized_rms:.3f}. "
        )

        url = "https://slack.com/api/files.upload"
        headers = {"Authorization": f"Bearer {self.token}"}
        data = {"channels": self.channel, "initial_comment": message}

        try:
            with open(recording_path, "rb") as f:
                files = {"file": f}
                response = requests.post(
                    url, headers=headers, data=data, files=files
                )

            result = response.json()
            if not result.get("ok", False):
                config.logger.error(
                    "Error sending to Slack: "
                    f"{result.get('error', 'Unknown error')}"
                )
                return False

            return True
        except Exception as e:
            config.logger.error(f"Error sending notification to Slack: {e}")
            return False
