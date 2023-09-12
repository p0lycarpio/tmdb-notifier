from dataclasses import dataclass
from typing import Optional

from Session import HTTPSession


@dataclass
class Movie:
    id: int
    title: str
    year: int
    overview: Optional[str] = None
    image: Optional[str] = None
    poster: Optional[str] = None
    runtime: Optional[int] = None


@dataclass
class Watchlist:
    ids: set[str]
    movies: list[Movie]


class TheMovieDatabase:
    def __init__(self, api_key, token, userid, language) -> None:
        self.base_url = "https://api.themoviedb.org"

        self.token = token
        self.userid = userid
        self.__http = HTTPSession()

        self.query_params = {"api_key": api_key, "language": language}

    def get_watchlist(self) -> Watchlist:
        def get_one_page(page: int = 1) -> dict:
            url = f"{self.base_url}/4/account/{self.userid}/movie/watchlist"
            auth = f"Bearer {self.token}"
            headers = {"Authorization": auth}
            params = self.query_params
            params["page"] = page

            response = self.__http.request("GET", url, headers=headers, params=params)
            return response.json()

        def get_all_watchlist_results(total_pages) -> dict:
            all_results = {"results": []}
            for page in range(1, total_pages + 1):
                response = get_one_page(page)
                all_results["results"].extend(response["results"])
                all_results["total_results"] = response["total_results"]

            return all_results

        fetch = get_one_page()
        all_movies = get_all_watchlist_results(fetch["total_pages"])
        print("Watchlist retrieved")

        ids = set(str())
        movies = list()
        for movie in all_movies["results"]:
            ids.add(str(movie.get("id")))
            movies.append(
                Movie(
                    id=movie.get("id"),
                    title=movie.get("title"),
                    year=movie.get("release_date")[0:4],
                )
            )

        return Watchlist(ids, movies)

    def get_movie(self, movie_id: int) -> Movie:
        url = f"{self.base_url}/3/movie/{movie_id}"

        response = self.__http.request("GET", url, params=self.query_params)
        response = response.json()

        return Movie(
            id=response["id"],
            title=response["title"],
            year=response["release_date"][0:4],
            overview=response["overview"],
            image=response["backdrop_path"],
            poster=response["poster_path"],
            runtime=response["runtime"],
        )

    def get_providers(self, movie_id: int) -> set:
        url = f"{self.base_url}/3/movie/{movie_id}/watch/providers"

        response = self.__http.request("GET", url, params=self.query_params)
        response = response.json()

        providers = set()

        if response.get("results", {}).get("FR", {}).get("flatrate") is not None:
            flatrate_providers = response["results"]["FR"]["flatrate"]
            for provider in flatrate_providers:
                providers.add(provider["provider_name"])

        return providers
