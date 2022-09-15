# immotest

a test

<!-- toc -->

- [Requirements](#requirements)
- [Development](#development)
  * [Local development](#local-development)
  * [Tests](#tests)
  * [Migrations](#migrations)

<!-- tocstop -->

## Requirements

* Python 3.8+

## Development

### Local development

First, create a `.env` file containing the settings:
```
DOMAIN=localhost
STACK_NAME=test
DOCKER_IMAGE_BACKEND=backend

# Backend
PROJECT_NAME=immotest
SECRET_KEY=xyz
FIRST_SUPERUSER=admin@example.com
FIRST_SUPERUSER_PASSWORD=zyx
LOG_LEVEL=debug
FETCH_ARTIST_DELAY=30.0
# Spotify API
SPOTIFY_CLIENT_ID=xyz
SPOTIFY_CLIENT_SECRET=zyx

# Postgres
POSTGRES_SERVER=db
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=app
SQLALCHEMY_DATABASE_URI=postgresql+asyncpg://postgres:postgres@db/app

INSTALL_DEV=false
```

Then, start the stack with Docker Compose:
```bash
# Build services
docker-compose build

# Create and start containers
docker-compose up -d

# Show the logs of the API backend (and background Spotify task)
docker-compose logs -f api
```

## Operation

Open your browser and interact with the API via:
* Automatic interactive documentation with Swagger UI: http://localhost:8080/docs

And interact with the DB via :
* pgWeb DB admin: http://localhost:8081/

**Nota Bene**: the Spotify connector does not refresh its token. So it will stop working when it expires (one hour).
If needed, the functionality to refresh it could be addded.


### Tests

Start the stack & run tests with this command:

```Bash
./scripts/test-local.sh
```

If your stack is already up, you just want to run the tests, you can use:

```bash
docker-compose exec api /app/scripts/tests-start.sh
```

### Migrations

After changing a model (for example, adding a column), create a revision, e.g.:
```bash
docker-compose run api alembic revision --autogenerate -m "Add column last_name to User model"
```

After creating the revision, run the migration in the database (this is what will actually change the database):
```bash
$ docker-compose run api alembic upgrade head
```
