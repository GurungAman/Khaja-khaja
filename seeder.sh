#!/bin/sh
python manage.py makemigrations
python manage.py migrate
python manage.py flush
python manage.py shell < populate.py