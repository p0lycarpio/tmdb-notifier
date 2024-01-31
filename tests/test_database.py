import pathlib
import json

import pytest

from tmdb_notifier.api import TheMovieDatabase
from tmdb_notifier.database import Database

def _load_fixture(filename: str) -> str:
    return pathlib.Path(__file__).parent.joinpath("fixtures", filename).read_text()

@pytest.fixture
def tmdb():
    return TheMovieDatabase(
        token="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9",
        userid="username",
        language="en-US")

@pytest.fixture
def db():
    return Database("./tests/__pycache__/tmdb.db")

def test_empty_database(db):
    try:
        db.get("watchlist")
    except KeyError as e:
        assert str(e) == "b'watchlist'"
    else:
        assert False, "Expected KeyError to be raised"

def test_compare_and_update_watchlist(db, tmdb):
    mock = json.loads(_load_fixture("watchlist.json"))
    watchlist = tmdb.get_watchlist(mock)
    watchlist_diff = db.compare_and_update("watchlist", watchlist.ids)
    assert watchlist_diff[0] == {695, 6977}
    assert watchlist_diff[1] == 2
    assert db.get("watchlist") == watchlist.ids

def test_compare_and_update_watchlist_with_no_changes(db, tmdb):
    mock = json.loads(_load_fixture("watchlist.json"))
    watchlist = tmdb.get_watchlist(mock)
    watchlist_diff = db.compare_and_update("watchlist", watchlist.ids)
    assert watchlist_diff[0] == set()
    assert watchlist_diff[1] == 0
    assert db.get("watchlist") == watchlist.ids

def test_compare_and_update_watchlist_new_id(db, tmdb):
    watchlist_diff = db.compare_and_update("watchlist", {123})
    assert watchlist_diff[0] == {123}
    assert watchlist_diff[1] == 3
    assert db.get("watchlist") == {123}

def test_compare_and_update_providers(db, tmdb):
    mock = json.loads(_load_fixture("providers.json"))
    providers = tmdb.get_providers(0, mock)
    providers_diff = db.compare_and_update("movie:6977:providers", providers)
    assert providers_diff[1] == 7
    assert db.get("movie:6977:providers") == providers

def test_cleanup_movies(db):
    db.cleanup()
    try:
        db.get("movie:6977:providers")
    except KeyError as e:
        assert str(e) == "b'movie:6977:providers'"
    else:
        assert False, "Expected KeyError to be raised"

def test_close_and_delete(db):
    db.close()
    pathlib.Path("./tests/__pycache__/tmdb.db").unlink()
    assert not pathlib.Path("./tests/__pycache__/tmdb.db").exists()
