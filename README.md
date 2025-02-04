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
   docker exec -it large-application-template-backend-development make
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
    docker build -f docker/production/Dockerfile -t large-application-template-backend-production --build-arg {REQUIRED ARGUMENTS} .
    ```

The built image can be used as image for:
- `application` - `run-production.sh` as
[Docker CMD](https://docs.docker.com/engine/reference/builder/#cmd)
to run application
- `worker` - `run-worker.sh` as `Docker CMD` to run worker

#### Required build arguments are:
`POSTGRES_DB_HOST` - Host of the postgres database  
`POSTGRES_DB_PORT` - Port of the postgres database  
`POSTGRES_DB_NAME` - Name of the postgres database  
`POSTGRES_DB_USER` - User of the postgres database  
`POSTGRES_DB_PASSWORD` - Password of the postgres database  
`BROKER_URL` - URL of broker passing messages between application and worker  
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

## Known issues

1. For
   [Chrome](https://www.google.com/chrome/)/
   [Chromium](https://www.chromium.org/chromium-projects/)
   web-browsers the application is not available over `0.0.0.0` address (development environment),
   because `Private Network Access` is disabled for `HTTP` protocol for those browsers.
   More details can be found
   [here](https://bugs.chromium.org/p/chromium/issues/detail?id=1300021).
   Nevertheless, the application still can be accessed over `localhost` address.
2. Running development environment on `Windows` may require additional steps to be taken.
   scripts in `docker/development/scripts/` path may not be found, due to invalid `EOF` characters in shell scripts.
   (more details can be found
   [here](https://stackoverflow.com/questions/2920416/configure-bin-shm-bad-interpreter)).
   
   There are a few solutions to this issue:
   1) Change `EOF` characters in shell scripts from `CRLF` (Windows) format to `LF` (Unix) format manually
   2) If a shell script is used to run a python file and the following error happens:
      ```shell
      env: python\r: No such file or directory
      ```
      Change `EOF` characters from `CRLF` (Windows) format to `LF` (Unix) format manually in the python file used in the shell script. 
   3) Run 
   [dos2unix](https://dos2unix.sourceforge.io)
   program on scripts in `docker/development/scripts/` path
