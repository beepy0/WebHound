import os
import platform
from celery import Celery
from django.conf import settings


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'WebHound.settings')

# celery won't work properly on Windows without this
if platform.system() == 'Windows':
    os.environ.setdefault('FORKED_BY_MULTIPROCESSING', '1')

app = Celery('WebHound', broker='amqp://')
# app = Celery('WebHound', broker='amqp://ozjuwkon:iT1MW6mGJPkCVjhqNK4cXgSACs1PNHtp@baboon.rmq.cloudamqp.com/ozjuwkon')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks(settings.INSTALLED_APPS)
