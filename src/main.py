import os
import logging
from datetime import timedelta

import utils

from Database import Database
from Notifier import Notifier
from Session import HTTPSession
from TheMovieDatabase import TheMovieDatabase, Watchlist


if __name__ == "__main__":
    loglevel = os.environ.get('LOGLEVEL', 'INFO').upper()
    logging.basicConfig(level=loglevel, format="%(asctime)s [%(levelname)s] %(message)s")
    logger = logging.getLogger("app")

    utils.check_env_vars(["TMDB_API_KEY", "TMDB_TOKEN", "TMDB_USERID", "WEBHOOK_URL"])

    db = Database(timedelta(weeks=2))
    http = HTTPSession()
    tmdb = TheMovieDatabase(
        api_key=os.getenv("TMDB_API_KEY"),
        token=os.getenv("TMDB_TOKEN"),
        userid=os.getenv("TMDB_USERID"),
        language=os.getenv("LANGUAGE", "fr-FR"),
    )

    notification = Notifier(webhook_url=os.getenv("WEBHOOK_URL"))
    services_filter = os.getenv("SERVICES", "").split(",")

    watchlist: Watchlist = tmdb.get_watchlist()
    watchlist_diff = db.compare_and_update("watchlist", watchlist.ids)[1]

    nb = len(watchlist.ids)
    changes = 0
    logger.info(f"Search providers for {nb} movies...")
    for idx, movie in enumerate(watchlist.movies, start=1):
        providers = tmdb.get_providers(movie.id)
        diff = utils.search_in(reference=list(services_filter),
                               search=db.compare_and_update(f"movie:{movie.id}:providers", providers)[0])
        if diff != set():
            services = utils.readable_list([provider for provider in diff])
            movie = tmdb.get_movie(movie.id)

            logger.info(f"New providers for {movie.title} ({movie.year}) : {services}")
            changes += 1
            message = notification.create_discord_message(
                movie=movie, services=services
            )
            notification.send_webhook(
                json_data=message, title=f"{movie.title} ({movie.year})"
            )

    logger.info(
        f"{nb} movies processed. {watchlist_diff} watchlist changes, {changes} movies with new providers and {nb-changes} non-updated.\n"
    )
    exit(0)
