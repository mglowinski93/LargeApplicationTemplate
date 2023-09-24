#!/bin/bash
set -e

# Run the worker.
exec celery -A modules.common.adapters.task_dispatchers.celery.task_dispatcher worker --loglevel=WARNING
