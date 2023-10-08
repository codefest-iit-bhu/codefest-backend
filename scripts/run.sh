#!/bin/sh

set -e

python manage.py collectstatic --noinput
python manage.py migrate
python manage.py populate_userinfo

gunicorn -w 4 --bind 127.0.0.1:8000 --timeout 120 codefest.wsgi

exec "$@"
