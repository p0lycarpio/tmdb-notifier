import requests
import json
from jsonpath_ng import jsonpath, parse

import config as _

base_url = "https://api.themoviedb.org"

def getQueryParams() -> dict:
    return {
        "api_key": _.tmdb_api_key,
        "language": "fr-FR"
    }

def Watchlist() -> list:
    url  = f"{base_url}/4/account/{_.tmdb_userid}/movie/watchlist"
    auth = f"Bearer {_.tmdb_token}"
    headers = {'Authorization': auth}
    
    response = requests.request("GET", url, headers=headers, params=getQueryParams())
    if response.status_code != 200: return
    response = response.json()
    
    print("Watchlist retrieved")
    watchlist = []
    for movie in response["results"]:
        watchlist.append(movie.get("id"))
    return watchlist


def Providers(movie_id) -> list:
    url = f"{base_url}/3/movie/{movie_id}/watch/providers"
    
    response = requests.request("GET", url, params=getQueryParams())
    if response.status_code != 200: return
    response = response.json()

    providers, selector, names = [], [], []
    expression = parse("$.results.FR.flatrate")
    for match in expression.find(response):
        selector = match.value

    if selector != None:
        for provider in selector:
            providers.append(provider)
            names.append(provider["provider_name"])
    return providers

def Movie(movie_id) -> dict:
    url = f"{base_url}/3/movie/{movie_id}"
    
    response = requests.request("GET", url, params=getQueryParams())
    if response.status_code != 200: return
    return response.json()