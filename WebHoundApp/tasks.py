import csv, io
from celery import shared_task

from .models import Trace


@shared_task
def trace_with_sherlock(name):
    print(f'This is the celery task executing for {name}..')
    return
