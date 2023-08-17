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
3. Open `http://localhost:8000` in browser.

#### Running tests

1. Build development environment as described above.
2. Execute `docker exec -it  large-application-template-backend-development make`.
