#!/bin/sh
python manage.py makemigrations
python manage.py migrate
python manage.py shell < populate.py
python manage.py collectstatic --noinput