#!/bin/sh

python manage.py makemigrations address --noinput
python manage.py migrate address --noinput
python manage.py makemigrations users --noinput
python manage.py migrate users --noinput
python manage.py makemigrations configs --noinput
python manage.py migrate configs --noinput
python manage.py migrate --noinput
python manage.py collectstatic --noinput

DJANGO_SUPERUSER_EMAIL=admin23@gmail.com DJANGO_SUPERUSER_PASSWORD=password python manage.py createsuperuser --no-input
gunicorn logs_sports.wsgi:application --bind 0.0.0.0:8000
