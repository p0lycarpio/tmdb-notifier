import os
import re
import logging

from src.models import Movie
from src.notifiers.apprise import Apprise
from src.notifiers.webhook import Webhook

class Notifiers:
    def __init__(self) -> None:
        self.logger = logging.getLogger("app:Notifiers")
        if os.getenv("APPRISE_URL"):
            self.notifier = Apprise(os.getenv("APPRISE_URL"))
        elif os.getenv("WEBHOOK_URL"):
            self.notifier = Webhook(os.getenv("WEBHOOK_URL"))
        else:
            raise ValueError("No notifier configured. Please set APPRISE_URL or WEBHOOK_URL")
    
    def send(self, movie: Movie, services):
        body = self.create_message(movie, services)
        self.notifier.send(movie=movie, title=f"TMDB Notification :", body=body)

    def create_message(self, movie: Movie, services: str) -> str:
        message = os.getenv("NOTIFICATION_BODY", f"{movie.title} ({movie.year}) is available on {services} !")
        variables = re.findall(r"\$\((.*?)\)", message)
        for variable in variables:
            if variable in movie.__dict__:
                self.logger.debug(f"Replacing $({variable}) with {movie.__dict__[variable]}")
                message = message.replace(f"$({variable})", str(movie.__dict__[variable]))
            else:
                message = message.replace("$(services)", str(services))
        return message