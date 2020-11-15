release: python3 manage.py migrate --settings=hasker.settings.production
web: gunicorn hasker.wsgi --preload --log-file -
