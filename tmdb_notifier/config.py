from dataclasses import dataclass
import dataclasses
import logging
import os
import tomllib

from tmdb_notifier.utils import flatten_dict


@dataclass
class ConfigValues:
    tmdb_token: str | None = None
    tmdb_userid: str | None = None
    webhook_url: str | None = None
    apprise_url: str | None = None
    notification_body: str | None = None
    services: str | list = ""
    webhook_type: str = "text/plain"
    language: str = "en-US"
    loglevel: str = "INFO"
    timezone: str = "UTC"
    cron: str = "0 20 * * *"

    def __init__(self, **kwargs):
        names = set([f.name for f in dataclasses.fields(self)])
        for k, v in kwargs.items():
            if k in names:
                setattr(self, k, v)
        self.__post_init__()

    def __post_init__(self):
        if self.tmdb_token is None or self.tmdb_token == "":
            raise ValueError("No TMDB token provided")
        if self.tmdb_userid is None or self.tmdb_userid == "":
            raise ValueError("No TMDB user ID provided")
        if self.services != "":
            self.services = [s.strip() for s in self.services.split(",")]  # type: ignore


class Configuration:
    def __init__(self, file: str = "/data/config.toml", **kwargs):
        self.logger = logging.getLogger("app:Configuration")
        self.file = file
        if kwargs:
            self.config = ConfigValues(**kwargs)
        else:
            self.load_config()

    def __repr__(self):
        return self.config.__repr__()

    def load_config(self):
        config = {}
        # Load configuration from TOML file and flatten it
        if os.path.isfile(self.file):
            self.logger.info(f"Loading configuration from {self.file}")
            with open(self.file, "rb") as f:
                config = flatten_dict(tomllib.load(f))

        # Load configuration from environment variables
        for key, value in os.environ.items():
            key = key.lower()
            if key in ConfigValues.__annotations__:
                config[key] = value

        # Map values to configuration attributes
        self.config = ConfigValues(**config)

    ### Properties ###
    @property
    def tmdb_token(self):
        return self.config.tmdb_token

    @property
    def tmdb_userid(self):
        return self.config.tmdb_userid

    @property
    def webhook_url(self):
        return self.config.webhook_url

    @property
    def webhook_type(self):
        return self.config.webhook_type

    @property
    def apprise_url(self):
        return self.config.apprise_url

    @property
    def language(self):
        return self.config.language

    @property
    def services(self):
        return self.config.services

    @property
    def loglevel(self):
        return self.config.loglevel

    @property
    def notification_body(self):
        return self.config.notification_body

    @property
    def cron(self):
        return self.config.cron
