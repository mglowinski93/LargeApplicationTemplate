#!/bin/bash
set -e

# Run the database migrations.
cd migrations/ && alembic upgrade head && cd -

# Run the production server.
exec gunicorn "main:app" --bind :8000 \
    --name "large-application-template" \
    --workers 5 \
    --log-level="info" \
    --capture-output
