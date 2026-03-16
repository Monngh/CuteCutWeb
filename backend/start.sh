#!/bin/bash
echo "Starting Celery worker..."
celery -A app.worker.celery_app worker --loglevel=info &

echo "Starting Uvicorn backend..."
exec uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}
