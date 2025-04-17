FROM python:3.13-slim
LABEL org.opencontainers.image.authors="mglowinski93@gmail.com"

ENV PYTHONUNBUFFERED 1

# Declare build arguments -> can be defined during build time.
ARG POSTGRES_DB_HOST
ARG POSTGRES_DB_PORT
ARG POSTGRES_DB_NAME
ARG POSTGRES_DB_USER
ARG POSTGRES_DB_PASSWORD
ARG TZ
ARG BROKER_URL

ARG USER=TemplateUser
ARG GROUP=TemplateGroup
ARG SCRIPTS_DIR="/scripts/"
ARG APP_DIR="/app/"
ARG TESTS_DIR="${APP_DIR}/tests/"

# Define environment variables.
ENV POSTGRES_DB_HOST=${POSTGRES_DB_HOST}
ENV POSTGRES_DB_PORT=${POSTGRES_DB_PORT}
ENV POSTGRES_DB_NAME=${POSTGRES_DB_NAME}
ENV POSTGRES_DB_USER=${POSTGRES_DB_USER}
ENV POSTGRES_DB_PASSWORD=${POSTGRES_DB_PASSWORD}
ENV TZ=${TZ}
ENV BROKER_URL=${BROKER_URL}

# Fix error: debconf: delaying package configuration, since apt-utils is not installed
# More details: https://github.com/phusion/baseimage-docker/issues/319
ARG DEBIAN_FRONTEND=noninteractive
RUN \
  apt-get update -y && \
  apt-get install -y apt-utils 2>&1 | grep -v "debconf: delaying package configuration, since apt-utils is not installed"

RUN apt-get install -y --no-install-recommends \
  tzdata \
  build-essential \
  libpq-dev
# tzdata - package for setting timezone
# build-essential - package for building python packages
# libpq-dev - package for psycopg2-binary (postgres driver)
# Add linux packages to install here

COPY backend/ ${APP_DIR}
RUN rm -rf ${TESTS_DIR}
COPY docker/production/backend/scripts/ ${SCRIPTS_DIR}
WORKDIR ${APP_DIR}

RUN useradd -m -r --no-user-group ${USER} && groupadd ${GROUP} && usermod -g ${GROUP} ${USER} && usermod -aG users ${USER}
# -m option is for creating user home directory
# -r option is for creating system account
# -g option is for assigning user to primary group
# -aG options are for assiging user to secondary group
RUN chown -R ${USER}:${GROUP} ${APP_DIR} ${SCRIPTS_DIR}
USER $USER

ENV PATH="/home/${USER}/.local/bin:${PATH}"
# Adding user local bin to PATH. It's necessary to have python packages available, since they are installed with non-root user privileges.
# Variale $HOME is not used, becase it's not defined yet at this step.
RUN python -m pip install --upgrade --user --disable-pip-version-check pip
RUN pip3 install --user -r "${APP_DIR}/requirements/production.txt"

ENV ENVIRONMENT="production"
# Define, which configuration to use for flask application.
# See config.py file in scheduler service for more details.
ENV FLASK_DEBUG=0
# Disable Flask debugger for hot-reloading.
# More details at https://flask.palletsprojects.com/en/2.0.x/config/.
