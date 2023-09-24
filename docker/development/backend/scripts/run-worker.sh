#!/bin/bash
set -e

# Install python packages.
python -m pip install --upgrade --user --disable-pip-version-check pip
pip install -r /app/requirements/development.txt

# Run the worker.
# `Watchmedo` is part of `watchdog` package and reloads the worker on code changes.
exec watchmedo auto-restart \
    --patterns="*.py" \
    --recursive \
    --signal SIGTERM \
    -- celery -A modules.common.adapters.task_dispatchers.celery.task_dispatcher worker --loglevel=INFO
