import os
from dotenv import load_dotenv
import redis


def init():
    global tmdb_api_key, tmdb_token, tmdb_userid, webhook_url, cron, redis_port, db, base_url
    load_dotenv()

    tmdb_api_key = os.getenv("TMDB_API_KEY")
    tmdb_token = os.getenv("TMDB_TOKEN")
    tmdb_userid = os.getenv("TMDB_USERID")
    webhook_url = os.getenv("WEBHOOK_URL")
    cron = os.getenv("CRON", "0 20 * * *")
    redis_port = os.getenv("REDIS_PORT", 6379)

    for k, v in globals().items():
        if not k.startswith('_') and v == None:
            print(f"ERROR: {k.upper()} variable is not set !")
            exit()

    db = redis.Redis(port=redis_port,decode_responses=True)
    base_url = "https://api.themoviedb.org"