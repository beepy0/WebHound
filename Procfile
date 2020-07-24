release: python manage.py migrate
web: gunicorn WebHound.wsgi
worker: celery worker --app=tasks.app
