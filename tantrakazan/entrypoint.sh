#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $DB_HOST $DB_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

poetry run python tantrakazan/manage.py makemigrations --noinput
poetry run python tantrakazan/manage.py migrate --noinput
#poetry run python manage.py collectstatic --noinput
#poetry run gunicorn backpack_store.wsgi:application --bind 0.0.0.0:8000
poetry run python tantrakazan/manage.py runserver 0.0.0.0:8000