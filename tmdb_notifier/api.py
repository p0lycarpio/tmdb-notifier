import asyncio
import logging
import json
from aiohttp.client_exceptions import ClientResponseError

from dataclasses import dataclass

from tmdb_notifier.session import HTTPSession

from tmdb_notifier.models import Movie


@dataclass
class Watchlist:
    ids: set[int]
    movies: list[Movie]


def read_json_mock(file_name: str) -> dict:
    with open(file_name, "r") as f:
        file_content = f.read()
        return json.loads(file_content)


class TheMovieDatabase:
    def __init__(self, token, userid, language, http: HTTPSession) -> None:
        self.base_url = "https://api.themoviedb.org/"
        self.token = token
        self.userid = userid
        self.country = language[3:5] or language[0:2].upper()

        self.logger = logging.getLogger("app:TheMovieDatabase")
        self.http = http

        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Accept": "application/json",
        }
        self.query_params = {"language": language}

    async def __aenter__(self):
        return self

    async def __aexit__(self):
        """Close the aiohttp session."""
        await self.http.close()

    async def get_watchlist(self, all_movies=None) -> Watchlist:
        async def get_one_page(page: int = 1) -> dict:
            url = f"{self.base_url}/3/account/{self.userid}/watchlist/movies"
            params = self.query_params.copy()
            params["page"] = page  # type: ignore

            try:
                async with self.http.request("GET", url, headers=self.headers, params=params) as response:
                    return await response.json()
            except ClientResponseError as e:
                self.logger.error(
                    f"Error while retrieving watchlist page {page} of {self.userid}: {e}"
                )
                raise e
            else:
                self.logger.debug(f"Watchlist page {page} of {self.userid} retrieved")

        async def get_all_watchlist_results(total_pages) -> dict:
            all_results = {"results": []}
            tasks = [get_one_page(page) for page in range(1, total_pages + 1)]
            responses = await asyncio.gather(*tasks)
            for response in responses:
                all_results["results"].extend(response["results"])
            all_results["total_results"] = responses[0]["total_results"] if responses else 0 # type: ignore

            self.logger.info("Watchlist retrieved")
            return all_results

        if not all_movies:
            fetch = await get_one_page()
            all_movies = await get_all_watchlist_results(fetch["total_pages"])

        ids = set()
        movies = list()
        for movie in all_movies["results"]:
            ids.add(int(movie.get("id")))
            movies.append(Movie(movie))

        return Watchlist(ids, movies)

    async def get_movie(self, movie_id: int, response=None) -> Movie:
        url = f"{self.base_url}/3/movie/{movie_id}"

        if not response:
            try:
                async with self.http.request("GET", url, headers=self.headers, params=self.query_params) as response:
                    response = await response.json()
                    self.logger.debug(f"Movie {movie_id} {response['title']} retrieved")
            except ClientResponseError as e:
                self.logger.error(f"Error while retrieving movie {movie_id}: {e}")
                raise e

        return Movie(response)

    async def get_credits(self, movie_id: int, response=None) -> dict:
        url = f"{self.base_url}/3/movie/{movie_id}/credits"
        if not response:
            try:
                async with self.http.request("GET", url, headers=self.headers, params=self.query_params) as response:
                    response = await response.json()
                    self.logger.debug(f"Credits for movie {movie_id} retrieved")
            except ClientResponseError as e:
                self.logger.error(
                    f"Error while retrieving credits for movie {movie_id}: {e}"
                )
                raise e

        return response

    async def get_providers(self, movie_id: int, response=None) -> set:
        url = f"{self.base_url}/3/movie/{movie_id}/watch/providers"

        if not response:
            try:
                async with self.http.request("GET", url, headers=self.headers, params=self.query_params) as response:
                    response = await response.json()
                    self.logger.debug(f"Providers for movie {movie_id} retrieved")
            except ClientResponseError as e:
                self.logger.error(
                    f"Error while retrieving providers for movie {movie_id}: {e}"
                )
                raise e

        providers = set()

        if (
            response.get("results", {}).get(self.country, {}).get("flatrate")
            is not None
        ):
            flatrate_providers = response["results"][self.country]["flatrate"]
            for provider in flatrate_providers:
                providers.add(provider["provider_name"])

        return providers
