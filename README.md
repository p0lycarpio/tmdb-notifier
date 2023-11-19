# tmdb-notifier

Monitor [TMDB](https://www.themoviedb.org/) watchlist and notify you when a movie is available on streaming services in your country.

> Availability data for movies on streaming services are provided by **JustWatch**. 

## Requierements

- Docker
- TMDB account and a [API key](https://www.themoviedb.org/settings/api)
- Webhook url (ex: Discord)

### Architectures

The architectures supported by this image are:

| Architecture | Available | Dockerfile |
| :----: | :----: | ---- |
| x86-64 | ✅ | Dockerfile |
| arm64 | ✅ | Dockerfile.aarch64 |
| armhf | ❌ | |


## Get started

Clone the repo and build the Doker image with `docker build -t tmdb-notifier -f Dockerfile .`

Create an `.env` file or specify environnement variables with `-e` in the following command. See [Environment variables](#environment-variables).

### Start the container

```bash
docker run -d \
    --env-file .env \
    --name tmdb-notifier tmdb-notifier
```

## Environment variables

- **WEBHOOK_URL**: URL of Discord webhook channel to send notification
- *CRON*: crontab trigger rules. Default : `0 20 * * *`
- **TMDB_TOKEN**: TMDB bearer token
- **TMDB_USERID**: TMDB username of the watchlist to monitor
- *LANGUAGE*: availability of films in your country. Default to `fr-FR`
- *SERVICES*: filter for streaming services separated by comma. Example: `Canal+,Disney Plus,Netflix`
- *TZ* : timezone. Default : `UTC`
- *LOGLEVEL* stdout verbosity. Default to `INFO`

## Contributing

Contributors, welcome ! Fork the repo and open PRs.

### Testing with JSON

```bash
docker run --rm \
    --env-file .env \
    --name tmdb-notifier -v $(pwd)/json/:/json/ tmdb-notifier
```

### TODO

- [ ] Migrate to [apprise](https://github.com/caronc/apprise) for implement more notifiers
- [ ] Allow user to modify notification body
- [x] Create filters for streaming services
- [ ] *TV series support ?*
