import requests

import config as _
import tmdb

def createWebhookContent(movie_id: str, services: str):
    movie = tmdb.Movie(movie_id)

    message = f"**{movie['title']}** ({str(movie['release_date'])[0:4]}) est disponible sur {services} !"
    movie_url = f"https://www.themoviedb.org/movie/{movie_id}"
    image = f"https://image.tmdb.org/t/p/w500{movie['backdrop_path']}"
    embed = {
      "title": movie['title'],
      "url": movie_url,
      "description": movie['overview'],
      "image": {
        "url": image
      }
    }
    body = {
        "content": message,
        "username": "TMDB",
        "avatar_url": "https://pbs.twimg.com/profile_images/1243623122089041920/gVZIvphd_400x400.jpg",
        "embeds" : [embed]
        }
    return body

def sendWebhook(json_data, movie):
    result = requests.post(_.webhook_url, json=json_data, headers={'Content-Type': 'application/json'})
    if 200 <= result.status_code < 300:
        print(f"Webhook sent for {movie}")
    else:
        print(f"Webhook not sent for {movie} with {result.status_code} response:\n{result.json()}")
