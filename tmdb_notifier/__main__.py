import logging
import time
import sys

from tmdb_notifier.utils import *

from tmdb_notifier.database import Database
from tmdb_notifier.notifiers import Notifiers
from tmdb_notifier.session import HTTPSession
from tmdb_notifier.api import TheMovieDatabase, Watchlist
from tmdb_notifier.config import Configuration

if __name__ == "__main__":
    # Return the value of a configuration attribute
    if len(sys.argv) > 1:
        print(getattr(Configuration(), sys.argv[1]))
        exit(0)
    
    config = Configuration()
    logging.basicConfig(
        level=config.loglevel, format="%(asctime)s [%(levelname)s] %(message)s"
    )
    logger = logging.getLogger("app")

    db = Database("/data/tmdb.db")
    http = HTTPSession()
    tmdb = TheMovieDatabase(
        token=config.tmdb_token,
        userid=config.tmdb_userid,
        language=config.language,
    )
    notification = Notifiers(configuration=config)

    watchlist: Watchlist = tmdb.get_watchlist()
    watchlist_diff = db.compare_and_update("watchlist", watchlist.ids)[1]

    nb = len(watchlist.ids)
    changes = 0
    logger.info(f"Search providers for {nb} movies...")
    for idx, movie in enumerate(watchlist.movies, start=1):
        providers = tmdb.get_providers(movie.id)
        diff = search_in(
            reference=list(config.services),
            search=db.compare_and_update(f"movie:{movie.id}:providers", providers)[0],
        )
        if diff != set():
            services = readable_list([provider for provider in diff])
            movie = tmdb.get_movie(movie.id)
            movie.set_credits(tmdb.get_credits(movie.id))
            logger.info(f"New providers for {movie.title} ({movie.year}) : {services}")
            notification.send(movie=movie, services=services)
            time.sleep(0.1)  # Avoid rate limit. wait 100ms between each request
            changes += 1

    logger.info(
        f"{nb} movies processed. {watchlist_diff} watchlist changes, {changes} movies with new providers and {nb-changes} non-updated.\n"
    )
    db.cleanup()
    db.close()
    exit(0)
