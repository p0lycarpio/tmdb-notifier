import logging
from abc import ABC, abstractmethod


class Notifier(ABC):
    @abstractmethod
    def __init__(self):
        self.logger = logging.getLogger("app:Notifier")

    @property
    def name(self):
        """Get notifier name"""
        return self.__class__.__name__

    def send(self, movie, title, body) -> None:
        """Send notification for new movie"""
        self.logger.debug("Sending %s Notification", self.name)
        self._send(movie, title, body)

    @abstractmethod
    def _send(self, movie, title, body) -> None:
        """Send movie information"""
