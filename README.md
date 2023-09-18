# LargeApplicationTemplate

Template for large application.

## Prerequisites

Running of this project locally requires the following tools to be
present on the host system:

* `docker` (version 23.05.0+)
* `docker compose` (version 2.21.0+)

## Development environment

To run development environment
1. Go into `docker/development/` folder
2. Execute
   
   ```bash
    docker compose up
   ```

### API description

API description can be accessed on development environment via `swagger` on 
http://localhost:8000/api/swagger/.

### Running tests

1. Build development environment as described above
2. Execute

   ```bash
   docker exec -it  large-application-template-backend-development make
   ```

#### Running performance tests

**`CAUTION`: Performance tests are not included
neither in automated tests nor in `CI/CD` pipeline.**

1. Build development environment as described above
2. Execute

   ```bash
   docker exec -it large-application-template-backend-development locust --locustfile "tests/performance/PATH_TO_TESTS_PER_MODULE" --host "http://localhost:8000"
   ```

3. Open http://localhost:8089/ in browser
4. [Optional step] Correct provided data
5. Run tests by [Locust](https://locust.io/) web interface

## Production environment

To build production
[docker image](https://docs.docker.com/engine/reference/commandline/images/)
:

1. Navigate to the root directory of the project.
2. Execute 

    ```bash
   docker build -t large-application-template-backend-production --build-arg {REQUIRED ARGUMENTS} .
    ```

#### Required build arguments are:
`POSTGRES_DB_HOST` - Host of the postgres database  
`POSTGRES_DB_PORT` - Port of the postgres database  
`POSTGRES_DB_NAME` - Name of the postgres database  
`POSTGRES_DB_USER` - User of the postgres database  
`POSTGRES_DB_PASSWORD` - Password of the postgres database  
`TZ` - TimeZone identifier (e.g. Europe/Warsaw)  

## Database migrations

Database migrations are managed by
[alembic](https://alembic.sqlalchemy.org/en/latest/).

#### Generating database migrations

1. Go into `migrations/` folder
2. Execute

   ```bash
   alembic revision --autogenerate -m "<MIGRATION_MESSAGE>"
    ```

#### Migrating database

1. Go into `migrations/` folder
2. Execute

    ```bash
    alembic upgrade head
     ```

## Working with repository

1. `backend` folder must be marked as `Sources Root` in `IDE` to make imports work
