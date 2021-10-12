#!/bin/sh

python manage.py migrate --noinput
python manage.py shell -c """from django.contrib.auth import get_user_model; \
from django.conf import settings; \
User=get_user_model(); \
User.objects.create_superuser('admin', 'admin@support-requests.pt', settings.ADMIN_PASS) """

exec "$@"