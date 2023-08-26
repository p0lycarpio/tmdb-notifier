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

### Testing with JSON

```bash
docker run --rm \
    --env-file .env \
    --name tmdb-notifier -v $(pwd)/json/:/json/ tmdb-notifier
```

## Environment variables

- **WEBHOOK_URL**: (str) - URL of Discord webhook channel to send notification
- *CRON*: (str) - crontab trigger rules. Default : "0 20 * * *"
- **TMDB_API_KEY**: TMDB v3 API key
- **TMDB_TOKEN**: TMDB v4 bearer token
- **TMDB_USERID**: username of the watchlist to monitor
- *TZ* : timezone
- *LANGUAGE*: (str)