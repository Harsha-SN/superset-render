#!/bin/bash

set -e

echo "======================================"
echo "Starting Superset"
echo "======================================"

echo "Running database upgrade..."
superset db upgrade

echo "Initializing Superset..."
superset init

echo "Starting Superset web server..."

exec gunicorn \
    -w 1 \
    -k gthread \
    --threads 2 \
    -b 0.0.0.0:${PORT:-10000} \
    "superset.app:create_app()"
