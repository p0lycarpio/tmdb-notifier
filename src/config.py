import os
from dotenv import load_dotenv
import redis


def init():
    global tmdb_api_key, tmdb_token, tmdb_userid, webhook_url, redis_port, db
    load_dotenv()

    print("\n=== TMDB Notifier starts ===\n")

    tmdb_api_key = os.getenv("TMDB_API_KEY")
    tmdb_token = os.getenv("TMDB_TOKEN")
    tmdb_userid = os.getenv("TMDB_USERID")
    webhook_url = os.getenv("WEBHOOK_URL")
    redis_port = os.getenv("REDIS_PORT", 6379)

    for k, v in globals().items():
        if not k.startswith('_') and v == None:
            print(f"ERROR: {k.upper()} variable is not set !")
            exit()

    db = redis.Redis(unix_socket_path="/var/run/redis.sock",
        socket_timeout=5, retry_on_timeout=True, decode_responses=True)