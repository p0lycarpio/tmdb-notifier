import logging
import sys

import asyncio

from tmdb_notifier.utils import *

from tmdb_notifier.database import Database
from tmdb_notifier.notifiers import Notifiers
from tmdb_notifier.session import HTTPSession
from tmdb_notifier.api import TheMovieDatabase, Watchlist
from tmdb_notifier.config import Configuration


async def main(db: Database) -> None:
    config = Configuration()
    logging.basicConfig(
        level=config.loglevel, format="%(asctime)s [%(levelname)s] %(message)s"
    )
    logger = logging.getLogger("app")

    http = HTTPSession()

    tmdb = TheMovieDatabase(
        token=config.tmdb_token,
        userid=config.tmdb_userid,
        language=config.language,
        http=http,
    )
    try:
        watchlist: Watchlist = await tmdb.get_watchlist()
        watchlist_diff = db.compare_and_update("watchlist", watchlist.ids)[1]

        nb = len(watchlist.ids)
        changes = 0
        logger.info(f"Search providers for {nb} movies...")

        async def process_movie(movie):
            providers = await tmdb.get_providers(movie.id)
            new_providers = db.compare_and_update(f"movie:{movie.id}:providers", providers)[0]
            logger.debug("New providers (diff) from db: " + str(new_providers))
            diff = search_in(
                reference=list(config.services),
                search=new_providers,
            )
            if diff != set():
                notifier = Notifiers(configuration=config, http=http)
                movie = await tmdb.get_movie(movie.id)
                if notifier.need_replace(movie.CREDITS, movie):
                    movie.set_credits(await tmdb.get_credits(movie.id))
                services = readable_list([provider for provider in diff])
                logger.info(f"New providers for {movie.title} ({movie.year}) : {services}")
                await notifier.send(movie=movie, services=services)
                return 1
            return 0

        tasks = [process_movie(movie) for movie in watchlist.movies]
        results = await asyncio.gather(*tasks)
        changes = sum(results)

        logger.info(
            f"{nb} movies processed. {watchlist_diff} watchlist changes, {changes} movies with new providers and {nb-changes} non-updated."
        )
        
    finally:
        await http.close()
    

if __name__ == "__main__":
    # Return the value of a configuration attribute
    if len(sys.argv) > 1:
        print(getattr(Configuration(), sys.argv[1]))
        exit(0)

    # Run the main function
    try:
        db = Database("/data/tmdb.db")
        asyncio.run(main(db))
    finally:
        db.cleanup()
        db.close()
    exit(0)