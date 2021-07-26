"""
ASGI config for khaja_khaja project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

import os, django

from django.core.asgi import get_asgi_application
from decouple import config

if config('environment') == 'dev':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'khaja_khaja.settings.developement')
elif config('environment') == 'prod':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'khaja_khaja.settings.production')

django.setup()
application = get_asgi_application()
