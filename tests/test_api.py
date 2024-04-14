import pathlib
import json

import pytest

from tmdb_notifier.api import TheMovieDatabase


def _load_fixture(filename: str) -> str:
    return pathlib.Path(__file__).parent.joinpath("fixtures", filename).read_text()


@pytest.fixture
def tmdb():
    return TheMovieDatabase(
        token="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9",
        userid="username",
        language="en-US",
    )


def test_get_watchlist(tmdb):
    mock = json.loads(_load_fixture("watchlist.json"))
    watchlist = tmdb.get_watchlist(mock)
    assert len(watchlist.movies) == 2
    assert watchlist.movies[0].id == 695
    assert watchlist.movies[1].id == 6977


def test_get_movie(tmdb):
    mock = json.loads(_load_fixture("movie.json"))
    movie = tmdb.get_movie(0, mock)
    assert movie.id == 6977
    assert movie.title == "No Country for Old Men"
    assert movie.year == 2007
    assert (
        movie.image == "https://image.tmdb.org/t/p/w500/kd9jFTTabg4xJpHDgxY0h8F9BzG.jpg"
    )
    assert movie.genres == "Crime, Drame & Thriller"
    assert movie.runtime == 122


def test_get_credits(tmdb):
    movie = tmdb.get_movie(0, json.loads(_load_fixture("movie.json")))
    credits = tmdb.get_credits(0, json.loads(_load_fixture("credits.json")))
    movie.set_credits(credits)
    assert movie.directors == "Joel Coen & Ethan Coen"
    assert movie.producers == "Joel Coen, Ethan Coen & Scott Rudin"


def test_get_providers(tmdb):
    mock = json.loads(_load_fixture("providers.json"))
    providers = tmdb.get_providers(0, mock)
    assert len(providers) == 7
    assert "Showtime" in providers
