#!/bin/sh

set -e

python manage.py collectstatic --noinput
python manage.py migrate

gunicorn -w 4 --bind 127.0.0.1:8000 --timeout 120 codefest.wsgi

exec "$@"
