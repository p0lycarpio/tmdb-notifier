# tmdb-notifier

Monitor [TMDB](https://www.themoviedb.org/) watchlist and notify you when a movie is available on streaming services in your country.

> Availability data for movies on streaming services are provided by **JustWatch**. 

## Requirements

- Docker
- TMDB account and a [API key](https://www.themoviedb.org/settings/api)
- Webhook or Apprise URL (ex: Discord)

### Architectures

The architectures supported by this image are:

| Architecture | Available | Dockerfile |
| :----: | :----: | ---- |
| x86-64 | ✅ | Dockerfile |
| arm64 | ✅ | Dockerfile.aarch64 |
| armhf | ❌ | |


## Get started

Clone the repo and build the Doker image with `docker build -t tmdb-notifier -f Dockerfile .`

Create an `.env` file or specify environnement variables with `-e` in the following command. See [Environment variables](#environment-variables) and [.env.sample](.env.sample) for complete example.

### Start the container

```bash
docker run -d \
    -v /path/to/localdata:/data
    --env-file .env \
    --name tmdb-notifier tmdb-notifier
```

## Environment variables

Variables in **bold** are required.

- **WEBHOOK_URL** or **APPRISE_URL**: webhook or [Apprise](https://github.com/caronc/apprise?tab=readme-ov-file#supported-notifications) URL to send notification
- **TMDB_TOKEN**: TMDB bearer token
- **TMDB_USERID**: TMDB username of the watchlist to monitor
- WEBHOOK_TYPE: Set to `application/json` for specify encoding. Default to `text/plain`
- NOTIFICATION_BODY: text content of notification. See [notifications variables](#notification-variables) for templating. Default notification: "`title` (`year`) is available on `services`! `TMDB link`"
- CRON: crontab trigger rules. Default : `0 20 * * *`
- LANGUAGE: availability of films in your country. Default to `en-US`
- SERVICES: filter for streaming services separated by comma. Example: `Canal+,Disney Plus,Netflix`
- TZ : timezone. Default : `UTC`
- LOGLEVEL stdout verbosity. Default to `INFO`

### Notification variables

You can customize the notification body with available following fields. Insert **$(variable)** in `NOTIFICATION_BODY` and it will be replaced.

| **Variable** | **Description** | **Example** |
|---|---|---|
| id | TMDB movie ID | 915935 |
| title | Movie title name | Anatomy of a Fall |
| original_title | Original movie name | Anatomie d'une chute |
| year | Movie year | 2023 |
| image | TMDB movie background URL | https://image.tmdb.org/t/p/w500/kszooR7v1TLFM4pzx6IkKq2jDAN.jpg |
| overview | Synopsis/summary | A woman is suspected of her husband’s murder, and their blind son faces a moral dilemma as the sole witness. |
| poster | Movie poster URL | https://image.tmdb.org/t/p/w500/kQs6keheMwCxJxrzV83VUwFtHkB.jpg |
| runtime | Runtime in minutes | 152 |
| genres |  | Drama & Mystery |
| languages |  | de, fr & en |
| original_language |  | fr |
| url | TMDB movie URL | https://www.themoviedb.org/movie/915935 |
| services | list of flarate services in your country | |


Other list variables about credits :
- actors
- directors
- writers
- producers
- composers


## Contributing

Contributors, welcome ! Fork the repo and open PRs.

### Testing with JSON

```bash
docker run --rm \
    --env-file .env \
    --name tmdb-notifier -v $(pwd)/json/:/json/ tmdb-notifier
```

### TODO

- [x] Migrate to [apprise](https://github.com/caronc/apprise) for implement more notifiers
- [x] Allow user to modify notification body
- [x] Create filters for streaming services
- [ ] Implement tests
- [ ] Build Docker image with actions and push to GHCR
- [ ] *TV series support ?*
