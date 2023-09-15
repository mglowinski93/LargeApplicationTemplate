# LargeApplicationTemplate

Template for large application.

## Prerequisites

Running of this project locally requires the following tools to be
present on the host system:

* `docker` (version 20.10.0+)
* `docker-compose` (version 1.27.0+)

## Development environment

To run development environment
1. Go into `docker/development` folder
2. Execute `docker-compose up`

### API description

API description can be accessed on development environment via `swagger` on 
http://localhost:8000/api/swagger/.

### Running tests

1. Build development environment as described above.
2. Execute `docker exec -it  large-application-template-backend-development make`.

#### Running performance tests

1. Build development environment as described above
2. Execute `docker exec -it large-application-template-backend-development locust --locustfile "tests/performance/PATH_TO_TESTS_PER_APP" --host "http://localhost:8000"`
3. Open http://localhost:8089/ in browser
4. [Optional step] Correct provided data.
5. Run tests by [Locust](https://locust.io/) web interface

## Production environment

To build production
[docker image](https://docs.docker.com/engine/reference/commandline/images/)
:

1. Navigate to root directory of the project.
2. Execute `docker build -t large-application-template-backend-production --build-arg {REQUIRED ARGUMENTS} .`

#### Required build arguments are:
`POSTGRES_DB_HOST` - Host of the postgres database  
`POSTGRES_DB_PORT` - Port of the postgres database  
`POSTGRES_DB_NAME` - Name of the postgres database  
`POSTGRES_DB_USER` - User of the postgres database  
`POSTGRES_DB_PASSWORD` - Password of the postgres database  
`TZ` - TimeZone identifier (e.g. Europe/Warsaw)  

## Database migrations

It's obligatory to navigate to proper folder,
due to that all
[alembic](https://alembic.sqlalchemy.org/en/latest/) commands
has to be called in place where `alembic.ini` is located.

#### Generating database migrations

1. Go into `migrations/` folder
2. Execute `alembic revision --autogenerate -m "<migration_message>"` command

#### Migrating database

1. Go into `migrations/` folder
2. Execute `alembic upgrade head` command
