#!/bin/bash

echo "In entrypoint.sh."

echo "Running pg_isready to check for Postgres availability"

until pg_isready -h $POSTGRES_HOST -p $POSTGRES_PORT -U $POSTGRES_USER
do
    echo "Waiting for postgres..."
    sleep 2;
done

echo "Apply database migrations."
python3 manage.py migrate

echo "Run collectstatic"
python3 manage.py collectstatic --noinput --verbosity=0

gunicorn evac_app.wsgi -b 0.0.0.0:8000

# Run command
echo "Running: $@"
exec "$@"