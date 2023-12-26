import logging
import json
from requests.exceptions import HTTPError

from dataclasses import dataclass
from typing import Optional

from src.Session import HTTPSession

from src.models import Movie


@dataclass
class Watchlist:
    ids: set[str]
    movies: list[Movie]

def read_json_mock(file_name: str) -> dict:
    with open(file_name, "r") as f:
        file_content = f.read()
        return json.loads(file_content)

class TheMovieDatabase:
    def __init__(self, token, userid, language, testmode=False) -> None:
        self.base_url = "https://api.themoviedb.org"

        self.token = token
        self.userid = userid
        self.country = language[3:5] or language[0:2].upper()
        
        self.__logger = logging.getLogger("app:TheMovieDatabase")
        self.__http = HTTPSession()

        self.headers = {"Authorization": f"Bearer {self.token}",
                        "Accept": "application/json"}
        self.query_params = {"language": language}
        self.testmode = testmode

    def get_watchlist(self) -> Watchlist:
        def get_one_page(page: int = 1) -> dict:
            url = f"{self.base_url}/3/account/{self.userid}/watchlist/movies"
            params = self.query_params
            params["page"] = page # type: ignore

            try:
                response = self.__http.request("GET", url, headers=self.headers, params=params)
                response.raise_for_status()
            except HTTPError as e:
                self.__logger.error(f"Error while retrieving watchlist page {page} of {self.userid}: {e}")
                raise e

            self.__logger.debug(f"Watchlist page {page} of {self.userid} retrieved")
            return response.json()

        def get_all_watchlist_results(total_pages) -> dict:
            all_results = {"results": []}
            for page in range(1, total_pages + 1):
                response = get_one_page(page)
                all_results["results"].extend(response["results"])
                all_results["total_results"] = response["total_results"]

            self.__logger.info("Watchlist retrieved")
            return all_results

        if self.testmode:
            all_movies = read_json_mock("/json/watchlist.json")
        else:
            fetch = get_one_page()
            all_movies = get_all_watchlist_results(fetch["total_pages"])
        
        ids = set(str())
        movies = list()
        for movie in all_movies["results"]:
            ids.add(str(movie.get("id")))
            movies.append(Movie(movie))

        return Watchlist(ids, movies)

    def get_movie(self, movie_id: int) -> Movie:
        url = f"{self.base_url}/3/movie/{movie_id}"

        if self.testmode:
            response = read_json_mock("/json/movie.json")
        else:
            try:
                response = self.__http.request("GET", url, headers=self.headers, params=self.query_params)
                response.raise_for_status()
            except HTTPError as e:
                self.__logger.error(f"Error while retrieving movie {movie_id}: {e}")
                raise e
            response = response.json()
        self.__logger.debug(f"Movie {movie_id} {response['title']} retrieved")

        return Movie(response)
    
    def get_credits(self, movie_id: int) -> dict:
        url = f"{self.base_url}/3/movie/{movie_id}/credits"
        try:
            response = self.__http.request("GET", url, headers=self.headers, params=self.query_params)
            response.raise_for_status()
        except HTTPError as e:
            self.__logger.error(f"Error while retrieving credits for movie {movie_id}: {e}")
            raise e

        response = response.json()
        self.__logger.debug(f"Credits for movie {movie_id} retrieved")

        return response

    def get_providers(self, movie_id: int) -> set:
        url = f"{self.base_url}/3/movie/{movie_id}/watch/providers"

        if self.testmode:
            response = read_json_mock("/json/providers.json")
        else:
            try:
                response = self.__http.request("GET", url, headers=self.headers, params=self.query_params)
                response.raise_for_status()
            except HTTPError as e:
                self.__logger.error(f"Error while retrieving providers for movie {movie_id}: {e}")
                raise e

            response = response.json()
        self.__logger.debug(f"Providers for movie {movie_id} retrieved")

        providers = set()

        if response.get("results", {}).get(self.country, {}).get("flatrate") is not None:
            flatrate_providers = response["results"][self.country]["flatrate"]
            for provider in flatrate_providers:
                providers.add(provider["provider_name"])
        
        return providers
