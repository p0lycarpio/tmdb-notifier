import os
import logging
from datetime import timedelta
import time

from src.utils import *

from src.Database import Database
from src.notifiers import Notifiers
from src.Session import HTTPSession
from src.TheMovieDatabase import TheMovieDatabase, Watchlist


if __name__ == "__main__":
    loglevel = os.environ.get('LOGLEVEL', 'INFO').upper()
    logging.basicConfig(level=loglevel, format="%(asctime)s [%(levelname)s] %(message)s")
    logger = logging.getLogger("app")

    check_env_vars(["TMDB_TOKEN", "TMDB_USERID"])

    db = Database(timedelta(weeks=2))
    http = HTTPSession()
    tmdb = TheMovieDatabase(
        token=os.getenv("TMDB_TOKEN"),
        userid=os.getenv("TMDB_USERID"),
        language=os.getenv("LANGUAGE", "fr-FR"),
    )

    notification = Notifiers()
    services_filter = os.getenv("SERVICES", "").split(",")

    watchlist: Watchlist = tmdb.get_watchlist()
    watchlist_diff = db.compare_and_update("watchlist", watchlist.ids)[1]

    nb = len(watchlist.ids)
    changes = 0
    logger.info(f"Search providers for {nb} movies...")
    for idx, movie in enumerate(watchlist.movies, start=1):
        providers = tmdb.get_providers(movie.id)
        diff = search_in(reference=list(services_filter),
                               search=db.compare_and_update(f"movie:{movie.id}:providers", providers)[0])
        if diff != set():
            services = readable_list([provider for provider in diff])
            movie = tmdb.get_movie(movie.id)
            movie.set_credits(tmdb.get_credits(movie.id))
            logger.info(f"New providers for {movie.title} ({movie.year}) : {services}")
            notification.send(movie=movie, services=services)
            time.sleep(0.1) # Avoid rate limit. wait 100ms between each request
            changes += 1

    logger.info(
        f"{nb} movies processed. {watchlist_diff} watchlist changes, {changes} movies with new providers and {nb-changes} non-updated.\n"
    )
    exit(0)
