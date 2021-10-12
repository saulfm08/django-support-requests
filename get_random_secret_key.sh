#!/bin/sh

python manage.py migrate --noinput
python manage.py shell -c """from django.core.management.utils import get_random_secret_key; \
print(\"New Django Secret Key: \");\
print(); \
print(f'DJANGO_SECRET_KEY=\"{get_random_secret_key()}\"');\
print(); \
print('Copy and paste this variable and value ^^^ into .env file');"""

exec "$@"