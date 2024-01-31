import pathlib
import json

import pytest

from unittest.mock import patch
from tmdb_notifier.notifiers import Notifiers
from tmdb_notifier.api import TheMovieDatabase


def _load_fixture(filename: str) -> str:
    return pathlib.Path(__file__).parent.joinpath("fixtures", filename).read_text()

@pytest.fixture
def tmdb():
    return TheMovieDatabase(
        token="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9",
        userid="username",
        language="en-US")

@pytest.fixture
def notifier():
    with patch.dict("os.environ", {"APPRISE_URL": "mqtt://user@hostname/topic"}):
        return Notifiers()

@patch("tmdb_notifier.notifiers.notifiers.logging")
def test_init_with_apprise_url(mock_logging):
    with patch.dict("os.environ", {"APPRISE_URL": "hassio://user@hostname/accesstoken"}):
        notifier = Notifiers()
        assert notifier.notifier is not None
        assert notifier.notifier.url == "hassio://user@hostname/accesstoken"
        assert mock_logging.getLogger.called

@patch("tmdb_notifier.notifiers.notifiers.logging")
def test_init_with_webhook_url(mock_logging):
    with patch.dict("os.environ", {"WEBHOOK_URL": "https://discord.com/api/webhooks/123/abc"}):
        notifier = Notifiers()
        assert notifier.notifier is not None
        assert notifier.notifier.url == "https://discord.com/api/webhooks/123/abc"
        assert mock_logging.getLogger.called

@patch("tmdb_notifier.notifiers.notifiers.logging")
def test_init_with_no_notifier_configured(mock_logging):
    with patch.dict("os.environ", clear=True):
        try:
            Notifiers()
        except ValueError as e:
            assert str(e) == "No notifier configured. Please set APPRISE_URL or WEBHOOK_URL"
        else:
            assert False, "Expected ValueError to be raised"
        assert mock_logging.getLogger.called

def test_create_simple_message(tmdb, notifier):
    mock = json.loads(_load_fixture("movie.json"))
    movie = tmdb.get_movie(0, mock)
    services = "Netflix"
    result = notifier.create_message(movie, services)
    assert result == f"{movie.title} ({movie.year}) is available on {services} !\n {movie.url}"

def test_create_custom_message(tmdb, notifier):
    mock = json.loads(_load_fixture("movie.json"))
    movie = tmdb.get_movie(0, mock)
    services = "Disney+"
    with patch.dict("os.environ", {"NOTIFICATION_BODY": "**$(title)** ($(year)) is available on $(services) in $(languages)"}):
        result = notifier.create_message(movie, services)
        assert result == f"**{movie.title}** ({movie.year}) is available on {services} in {movie.languages}"