#!/bin/sh

echo "Starting Superset..."

superset db upgrade

superset fab create-admin \
  --username admin \
  --firstname Superset \
  --lastname Admin \
  --email admin@example.com \
  --password "$ADMIN_PASSWORD" || true

superset init

echo "Starting Gunicorn..."

exec gunicorn \
  -w 1 \
  -k gthread \
  --threads 2 \
  -b 0.0.0.0:${PORT:-10000} \
  'superset.app:create_app()'
