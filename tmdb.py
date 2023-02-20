import os
import time
import ast
from datetime import datetime, timedelta
from jsonpath_ng import jsonpath, parse

import utils
import redis
import requests

from dotenv import load_dotenv

load_dotenv()

redis_port = os.getenv("REDIS_PORT", 6379)
db = redis.Redis(port=redis_port,decode_responses=True)
base_url = "https://api.themoviedb.org"


def Watchlist(tmdb_api_key, tmdb_token, tmdb_userid) -> list:
    url  = f"{base_url}/4/account/{tmdb_userid}/movie/watchlist"
    url += f"?api_key={tmdb_api_key}"
    auth = f"Bearer {tmdb_token}"
    headers = {'Authorization': auth}
    
    response = requests.request("GET", url, headers=headers)
    if response.status_code != 200: return
    
    print("Watchlist retrieved")
    watchlist = []
    for movie in response.json()["results"]:
        watchlist.append(movie.get("id"))
    return watchlist


def Providers(movie_id, tmdb_api_key) -> list:
    url = f"{base_url}/3/movie/{movie_id}/watch/providers"
    url += f"?api_key={tmdb_api_key}"  
    
    response = requests.request("GET", url)
    if response.status_code != 200: return

    providers, selector, names = [], [], []
    expression = parse("$.results.FR.flatrate")
    for match in expression.find(response.json()):
        selector = match.value

    if selector != None:
        for provider in selector:
            providers.append(provider)
            names.append(provider["provider_name"])
    return providers

def compare_database(object_name: str, requested_obj: list) -> list:
    """
    Compare the given object with database and returns differences.
    Updates the record in the databse if it doesn't exist or if it is outdated.
    """
    stored_obj = db.get(object_name)
    diff = []

    if stored_obj is not None:
        stored_obj = ast.literal_eval(stored_obj)
        diff = utils.find_difference(requested_obj, stored_obj)
    
    if stored_obj is None or diff != []:
        db.set(object_name, str(requested_obj), ex=timedelta(weeks=4))
        print(f"DB: {object_name} entry updated")
    
    return diff

def main():
    tmdb_api_key = os.getenv("TMDB_API_KEY")
    tmdb_token = os.getenv("TMDB_TOKEN")
    tmdb_userid = os.getenv("TMDB_USERID")

    updateWl = Watchlist(tmdb_api_key, tmdb_token, tmdb_userid)
    compare_database("watchlist", updateWl)

    nb = len(updateWl)
    print(f"\nSearch providers for {nb} movies :")
    for idx, movie_id in enumerate(updateWl, start=1):
        providers = Providers(movie_id, tmdb_api_key)
        diff = compare_database(movie_id, providers)
        services = [d['provider_name'] for d in diff if 'provider_name' in d]
        if(diff != []):
            print(f"{idx}/{nb} New providers for {movie_id} : {', '.join(services)}")
        else:
            print(f"{idx}/{nb} No providers updates for {movie_id}")
        time.sleep(.1)

if __name__ == "__main__":
    main()