import json
import logging

from aiohttp.client_exceptions import ClientResponseError

from tmdb_notifier.models import Movie
from tmdb_notifier.notifiers import Notifier
from tmdb_notifier.session import HTTPSession


class Webhook(Notifier):
    """Notifier for custom Webhooks"""

    def __init__(self, url, encoding, http: HTTPSession) -> None:
        self.logger = logging.getLogger("app:Webhook")
        self.http = http
        self.encoding = encoding
        self.url = url

    async def _send(self, movie: Movie, body: str) -> None:
        """Sends movie notification via configured Webhook endpoint"""
        if "json" in self.encoding:
            try:
                json_data = json.loads(body)
            except json.JSONDecodeError as e:
                self.logger.error(f"Error while parsing JSON: {e}")
                raise e
            body_data = None
        else:
            json_data = None
            body_data = bytes(body, encoding="utf-8")
        try:
            async with self.http.post(
                url=self.url,
                data=body_data,
                json=json_data,
                headers={"Content-Type": self.encoding},
            ):
                self.logger.info(f"Webhook sent for {movie.title}")
        except ClientResponseError as e:
            self.logger.error(f"Error while sending webhook for {movie.title}: {e}")
