import sys
import os

import pytest
from aiohttp import ClientSession as HTTPSession

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from tmdb_notifier.api import TheMovieDatabase

pytest_plugins = 'aiohttp.pytest_plugin'


@pytest.fixture
async def http_session(loop):
    async with HTTPSession() as session:
        yield session

@pytest.fixture
def tmdb(http_session):
    return TheMovieDatabase(
        token="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9",
        userid="username",
        language="en-US",
        http=http_session,
    )
