import json
import os
import logging

import requests

from tmdb_notifier.models import Movie
from tmdb_notifier.notifiers import Notifier


class Webhook(Notifier):
    """Notifier for custom Webhooks"""

    def __init__(self, url):
        self.logger = logging.getLogger("app:Webhook")
        self.url = url

    def _send(self, movie: Movie, title, body) -> None:
        """Sends movie notification via configured Webhook endpoint"""
        if os.getenv("WEBHOOK_TYPE", "") == "json":
            body = json.loads(body)
        try:
            result = requests.post(
                url=self.url,
                json=body,
                headers={"Content-Type": "application/json"},
            )
            result.raise_for_status()
            self.logger.info(f"Webhook sent for {movie.title}")
        except requests.exceptions.HTTPError as e:
            self.logger.error(f"Error while sending webhook for {movie.title}: {e}")
            raise e

    def __repr__(self) -> str:
        return f"Webhook: {self.url}"
