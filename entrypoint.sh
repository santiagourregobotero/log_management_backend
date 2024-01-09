#!/bin/sh

python manage.py makemigrations users --noinput
python manage.py migrate users --noinput
python manage.py makemigrations logs --noinput
python manage.py migrate logs --noinput
python manage.py migrate

DJANGO_SUPERUSER_EMAIL=admin23@gmail.com DJANGO_SUPERUSER_PASSWORD=password python manage.py createsuperuser --no-input
gunicorn logs.wsgi:application --bind 0.0.0.0:8000
