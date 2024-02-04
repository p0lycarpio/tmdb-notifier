from tmdb_notifier.config import Configuration


def test_load_config_from_file(tmp_path):
    config_file = tmp_path / "test.toml"
    config_file.write_text("[tmdb]\ntmdb_token = 'abc123'\ntmdb_userid = 'popcorn'\n")
    config = Configuration(file=str(config_file))
    assert config.tmdb_token == "abc123"
    assert config.tmdb_userid == "popcorn"


def test_load_config_from_environment_variables(monkeypatch):
    monkeypatch.setenv("TMDB_TOKEN", "def456")
    monkeypatch.setenv("TMDB_USERID", "butter")
    config = Configuration()
    assert config.tmdb_token == "def456"
    assert config.tmdb_userid == "butter"


def test_load_config_with_kwargs():
    config = Configuration(
        tmdb_token="abc", tmdb_userid="123", services="Netflix,Disney+"
    )
    assert config.tmdb_token == "abc"
    assert config.tmdb_userid == "123"
    assert config.services == ["Netflix", "Disney+"]
    assert type(config.services) == list
    assert config.language == "en-US"
