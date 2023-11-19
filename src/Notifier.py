import requests
import logging

from TheMovieDatabase import Movie


class Notifier:
    def __init__(self, webhook_url) -> None:
        self.webhook_url = webhook_url
        self.__logger = logging.getLogger("app:Notifier")

    def create_discord_message(self, movie: Movie, services: str) -> dict:
        message = f"**{movie.title}** ({movie.year}) est disponible sur {services} !"
        movie_url = f"https://www.themoviedb.org/movie/{movie.id}"
        image = f"https://image.tmdb.org/t/p/w500{movie.image}"
        embed = {
            "title": movie.title,
            "url": movie_url,
            "description": movie.overview,
            "image": {"url": image},
        }
        body = {
            "content": message,
            "username": "TMDB",
            "avatar_url": "https://pbs.twimg.com/profile_images/1243623122089041920/gVZIvphd_400x400.jpg",
            "embeds": [embed],
        }
        self.__logger.debug(f"Discord message body : {body}")
        return body

    def send_webhook(self, json_data, title):
        try:
            result = requests.post(
                self.webhook_url,
                json=json_data,
                headers={"Content-Type": "application/json"},
            )
            result.raise_for_status()
            self.__logger.info(f"Webhook sent for {title}")
        except requests.exceptions.HTTPError as e:
            self.__logger.error(f"Error while sending webhook for {title}: {e}")
            raise e

