import os
from typing import Any, Dict, List, Optional

import requests

from src.utils.config import Config

from .base import BaseNotifier


class SlackNotifier(BaseNotifier):

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
        slack_config = config.notifier_options.get("slack", {})
        token = (
            self.token or slack_config.get("token") or os.getenv("SLACK_TOKEN")
        )
        channel = (
            self.channel
            or slack_config.get("channel")
            or os.getenv("SLACK_CHANNEL")
        )

        if not token:
            config.logger.error(
                "Slack token not found. Notification will not be sent."
            )
            return False

        if not channel:
            config.logger.error(
                "No Slack channel specified. Notification will not be sent."
            )
            return False

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
        headers = {"Authorization": f"Bearer {token}"}
        data = {"channels": channel, "initial_comment": message}

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
