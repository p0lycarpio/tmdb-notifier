# tmdb-notifier

Watch TMDB watchlist and notify when a movie is available on streaming services.

## Docker

Build image, first `docker build -t tmdb-notifier .`

Run container

```bash
docker run -d \
    --env-file .env \
    --name tmdb-notifier tmdb-notifier
```

## Environment variables

- **DISCORD_WEBHOOK**: (str) - URL of Discord webhook channel to send notification
- **CRON**: (str) - crontab trigger rules
- **TMDB_API_KEY**: TMDB v3 API key
- **TMDB_TOKEN**: TMDB v4 bearer token
- **TMDB_USERID**: username of the watchlist to monitor
