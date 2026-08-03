#!/bin/bash
# Init script for Render: run DB migrations, then start the app/worker.
# Usage: ./init.sh web     (default)
#        ./init.sh worker   (celery)
#        ./init.sh flower   (flower UI)
set -e

# Run Alembic migrations against the database
if [ -n "$DATABASE_URL" ] || [ -n "$POSTGRES_PASSWORD" ]; then
    echo "Running database migrations..."
    alembic upgrade head
else
    echo "No DATABASE_URL set; skipping migrations."
fi

case "$1" in
    worker)
        exec celery -A workers.celery_app worker --loglevel=info --concurrency=4
        ;;
    flower)
        exec celery -A workers.celery_app flower --port=5555 --host=0.0.0.0
        ;;
    web|*)
        exec uvicorn main:app --host 0.0.0.0 --port=${PORT:-8000}
        ;;
esac
