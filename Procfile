release: python manage.py migrate
web: gunicorn WebHound.wsgi
worker: celery -A WebHoundApp worker -B --loglevel=info
