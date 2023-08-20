#!/bin/bash
set -e

# Install python packages.
python -m pip install --upgrade --user --disable-pip-version-check pip
pip install -r /app/requirements/development.txt

# Run the database migrations.
cd migrations/ && alembic upgrade head && cd -

# Run the development server.
exec flask run --host 0.0.0.0 --port 8000
