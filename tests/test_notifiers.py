import pathlib
import json

import pytest

from unittest.mock import patch
from tmdb_notifier.notifiers import Notifiers
from tmdb_notifier.config import Configuration


def _load_fixture(filename: str) -> str:
    return pathlib.Path(__file__).parent.joinpath("fixtures", filename).read_text()


@pytest.fixture
def config_apprise():
    return Configuration(
        tmdb_token="a",
        tmdb_userid="b",
        apprise_url="hassio://user@hostname/accesstoken",
    )


@pytest.fixture
def config_webhook():
    return Configuration(
        tmdb_token="a",
        tmdb_userid="b",
        webhook_url="https://discord.com/api/webhooks/123/abc",
        webhook_type="application/json",
        notification_body="**$(title)** ($(year)) is available on $(services) in $(languages)",
    )

@pytest.fixture
def config_webhook_credits():
    return Configuration(
        tmdb_token="a",
        tmdb_userid="b",
        webhook_url="https://discord.com/api/webhooks/123/abc",
        webhook_type="application/json",
        notification_body="**$(title)** ($(year)) from $(directors) is available on $(services) in $(languages)",
    )

@pytest.fixture
def notifier_apprise(config_apprise, http_session):
    return Notifiers(config_apprise, http_session)

@pytest.fixture
def notifier_webhook(config_webhook, http_session):
    return Notifiers(config_webhook, http_session)

@pytest.fixture
def notifier_webhook_credits(config_webhook_credits, http_session):
    return Notifiers(config_webhook_credits, http_session)


@pytest.mark.asyncio
@patch("tmdb_notifier.notifiers.notifiers.logging")
def test_init_with_apprise_url(mock_logging, config_apprise, http_session):
    notifier = Notifiers(config_apprise, http_session)
    assert notifier.notifier is not None
    assert notifier.notifier.url == "hassio://user@hostname/accesstoken"
    assert mock_logging.getLogger.called


@pytest.mark.asyncio
@patch("tmdb_notifier.notifiers.notifiers.logging")
def test_init_with_webhook_url(mock_logging, config_webhook, http_session):
    notifier = Notifiers(config_webhook, http_session)
    assert notifier.notifier is not None
    assert notifier.notifier.url == "https://discord.com/api/webhooks/123/abc"
    assert mock_logging.getLogger.called


@pytest.mark.asyncio
@patch("tmdb_notifier.notifiers.notifiers.logging")
def test_init_with_no_notifier_configured(mock_logging, http_session):
    with patch.dict("os.environ", clear=True):
        try:
            Notifiers(Configuration(tmdb_token="a", tmdb_userid="b"), http_session)
        except ValueError as e:
            assert (
                str(e)
                == "No notifier configured. Please set APPRISE_URL or WEBHOOK_URL"
            )
        else:
            assert False, "Expected ValueError to be raised"
        assert mock_logging.getLogger.called


@pytest.mark.asyncio
async def test_create_simple_message(tmdb, notifier_apprise):
    mock = json.loads(_load_fixture("movie.json"))
    movie = await tmdb.get_movie(0, mock)
    services = "Netflix"
    result = notifier_apprise.create_message(movie, services)
    assert (
        result
        == f"{movie.title} ({movie.year}) is available on {services} !\n {movie.url}"
    )


@pytest.mark.asyncio
async def test_create_custom_message(tmdb, notifier_webhook):
    mock = json.loads(_load_fixture("movie.json"))
    movie = await tmdb.get_movie(0, mock)
    services = "Disney+"
    result = notifier_webhook.create_message(movie, services)
    assert (
        result
        == f"**{movie.title}** ({movie.year}) is available on {services} in {movie.languages}"
    )


@pytest.mark.asyncio
async def test_need_replace_credits(tmdb, notifier_webhook_credits):
    mock = json.loads(_load_fixture("movie.json"))
    movie = await tmdb.get_movie(0, mock)
    print(movie.__dict__)
    assert notifier_webhook_credits.need_replace(["directors", "actors"], movie) == True
