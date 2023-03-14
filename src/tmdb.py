import requests
import json
from jsonpath_ng import jsonpath, parse

import config as _

def Watchlist() -> list:
    # url  = f"{base_url}/4/account/{_.tmdb_userid}/movie/watchlist"
    # url += f"?api_key={_.tmdb_api_key}"
    # auth = f"Bearer {_.tmdb_token}"
    # headers = {'Authorization': auth}
    
    # response = requests.request("GET", url, headers=headers)
    # if response.status_code != 200: return
    f =open("watchlist.json")
    response = json.load(f)
    
    print("Watchlist retrieved")
    watchlist = []
    for movie in response["results"]:
        watchlist.append(movie.get("id"))
    return watchlist


def Providers(movie_id) -> list:
    # url = f"{base_url}/3/movie/{movie_id}/watch/providers"
    # url += f"?api_key={_.tmdb_api_key}"  
    
    # response = requests.request("GET", url)
    # if response.status_code != 200: return
    f = open("providers.json")
    response = json.load(f)
    providers, selector, names = [], [], []
    expression = parse("$.results.FR.flatrate")
    for match in expression.find(response):
        selector = match.value

    if selector != None:
        for provider in selector:
            providers.append(provider)
            names.append(provider["provider_name"])
    return providers

def Movie(movie_id):
    """ url = f"{base_url}/3/movie/{movie_id}?language=fr-FR"
    url += f"?api_key={_.tmdb_api_key}"  
    
    response = requests.request("GET", url)
    if response.status_code != 200: return
    return response.content """
    f = open("movie.json")
    return json.load(f)