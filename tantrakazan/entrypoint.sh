#!/bin/sh

poetry run python tantrakazan/manage.py makemigrations --noinput
poetry run python tantrakazan/manage.py migrate --noinput
#poetry run python manage.py collectstatic --noinput
#poetry run gunicorn backpack_store.wsgi:application --bind 0.0.0.0:8000
poetry run python tantrakazan/manage.py runserver 0.0.0.0:8000