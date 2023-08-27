FROM python:3.11

RUN \
  apt-get update -y && \
  apt-get install -y apt-utils 2>&1 | grep -v "debconf: delaying package configuration, since apt-utils is not installed"
RUN apt-get install -y --no-install-recommends \
  tzdata \
  make
# tzdata - package for setting timezone
# make - package for running Makefile (needed for automated checks)

WORKDIR /app

ENV ENVIRONMENT="development"
# Define, which configuration to use for flask application.
# See config.py file in scheduler service for more details.
ENV FLASK_DEBUG=1
# Enable Flask debugger for hot-reloading.
# More details at https://flask.palletsprojects.com/en/2.0.x/config/.
ENV FLASK_APP="main.py"
# Defines file with Flask application.

CMD ["/scripts/run-development.sh"]
