release: python3 manage.py migrate --settings=hasker.settings.production
release: python3 manage.py initadmin --settings=hasker.settings.production
web: gunicorn hasker.wsgi --preload --log-file -
