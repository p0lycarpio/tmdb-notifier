import logging

import apprise
from apprise import AppriseAsset

from tmdb_notifier.models import Movie
from tmdb_notifier.notifiers import Notifier


class Apprise(Notifier):
    """
    Notifier for Apprise. \n
    For more information on Apprise visit\n
    https://github.com/caronc/apprise
    """

    def __init__(self, url):
        self.logger = logging.getLogger("app:Notifier")
        self.apprise = apprise.Apprise(
            asset=AppriseAsset(
                app_id="TMDB",
                app_desc="TMDB Notifier",
                app_url="https://github.com/p0lycarpio/tmdb-notifier",
                image_url_mask="https://pbs.twimg.com/profile_images/1243623122089041920/gVZIvphd_400x400.jpg",
            )
        )
        self.url = url

    def _send(self, movie: Movie, title, body) -> None:
        """Sends movie notification via configured Apprise URL"""
        url = self.url

        self.logger.debug("Apprise url: %s", url)
        self.logger.debug("Apprise title: %s", title)
        self.logger.debug("Apprise body: %s", body)

        self.apprise.add(self.url)
        try:
            self.apprise.notify(title=title, body=body)
            self.logger.error(f"Webhook sent for {movie.title}")
        except Exception as e:
            self.logger.error(f"Error while sending Apprise notification for {movie.title}: {e}")
            raise e
        self.apprise.clear()

    def __repr__(self) -> str:
        return f"Apprise: {self.url}"