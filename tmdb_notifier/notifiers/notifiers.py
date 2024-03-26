import re
import logging

from tmdb_notifier.models import Movie
from tmdb_notifier.notifiers.apprise import Apprise
from tmdb_notifier.notifiers.webhook import Webhook
from tmdb_notifier.config import Configuration


class Notifiers:
    def __init__(self, configuration: Configuration) -> None:
        self.logger = logging.getLogger("app:Notifiers")
        self.apprise = configuration.apprise_url
        self.webhook = configuration.webhook_url
        self.webhook_type = configuration.webhook_type
        self.notification_body = configuration.notification_body

        if self.apprise:
            self.notifier = Apprise(self.apprise)
        elif self.webhook:
            self.notifier = Webhook(self.webhook, self.webhook_type)
        else:
            raise ValueError(
                "No notifier configured. Please set APPRISE_URL or WEBHOOK_URL"
            )

    def send(self, movie: Movie, services: str):
        body = self.create_message(movie, services)
        self.notifier.send(movie, body)

    def get_message(self, movie: Movie, services: str) -> str:
        return (
            self.notification_body or
            f"{movie.title} ({movie.year}) is available on {services} !\n {movie.url}"
            )

    def create_message(self, movie: Movie, services: str) -> str:
        message = self.get_message(movie, services)
        if self.notification_body:
            variables = self.__find_variables(message)
            message = message.replace("$(services)", services)
            return self.__replace_variables(message, movie, variables)
        return message

    def __find_variables(self, message: str) -> list[str]:
        return re.findall(r"\$\((.*?)\)", message)
    
    def need_replace(self, variables: list, movie: Movie) -> bool:
        message = self.__find_variables(
            self.get_message(movie, "")
        )
        self.logger.debug(f"Variables in message: {message}")
        return any(item in variables for item in message)
    
    def __replace_variables(self, message: str, movie: Movie, variables: list) -> str:
        for variable in variables:
            if variable in movie.__dict__:
                self.logger.debug(
                    f"Replacing $({variable}) with {movie.__dict__[variable]}"
                )
                message = message.replace(
                    f"$({variable})", str(movie.__dict__[variable])
                )
        return message
