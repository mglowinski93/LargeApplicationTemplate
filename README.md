# LargeApplicationTemplate

Template for large application based on the 
[cosmicpython book](https://github.com/cosmicpython/book).

## Prerequisites

Running of this project locally requires the following tools to be
present on the host system:

* `docker` (version 20.10.0+)
* `docker-compose` (version 1.27.0+)

## Development environment

To run development environment
1. Go into `docker/development` folder.
2. Execute `docker-compose up`.

## API description

API description can be accessed on development environment via `swagger` on 
http://localhost:8000/api/swagger/.

## Running tests

1. Build development environment as described above.
2. Execute `docker exec -it  large-application-template-backend-development make`.

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
