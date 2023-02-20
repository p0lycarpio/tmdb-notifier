import json

f = open('watchlist.json')

watchlist = json.load(f)

tmdb_ids = []
for movie in watchlist["results"]:
    tmdb_ids.append(movie.get("id"))
print(tmdb_ids)
