import os
import time
import ast
from datetime import datetime, timedelta

import config as _
import tmdb
import utils
import webhook

def compare_database(object_name: str, requested_obj: list) -> list:
    """
    Compare the given object with database and returns differences.
    Updates the record in the databse if it doesn't exist or if it is outdated.
    """
    stored_obj = _.db.get(object_name)
    diff = []

    if stored_obj is not None:
        stored_obj = ast.literal_eval(stored_obj)
        diff = utils.find_difference(requested_obj, stored_obj)
    
    if stored_obj is None or diff != []:
        _.db.set(object_name, str(requested_obj), ex=timedelta(weeks=4))
        print(f"DB: {object_name} entry updated")
    
    return diff

def main():
    _.init()
    updateWl = tmdb.Watchlist()
    compare_database("watchlist", updateWl)

    nb = len(updateWl)
    print(f"\nSearch providers for {nb} movies :")
    for idx, movie_id in enumerate(updateWl, start=1):
        providers = tmdb.Providers(movie_id)
        diff = compare_database(movie_id, providers)
        services = [d['provider_name'] for d in diff if 'provider_name' in d]
        services = utils.readable_list(services)
        if(diff != []):
            print(f"{idx}/{nb} New providers for {movie_id} : {services}")
            message = webhook.createWebhookContent(movie_id, services)
            webhook.sendWebhook(message, movie_id)
        else:
            print(f"{idx}/{nb} No providers updates for {movie_id}")
        time.sleep(.1)

if __name__ == "__main__":
    main()