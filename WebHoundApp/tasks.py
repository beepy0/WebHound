import csv, io
import pytz
from datetime import datetime, timedelta
from celery import shared_task
from django.core.exceptions import ObjectDoesNotExist

from .models import Trace
from .config import errors


@shared_task
def trace_with_sherlock(name):
    try:
        trace = Trace.objects.get(pk=name)
    except ObjectDoesNotExist:
        raise KeyError(errors['no_name_in_db'])
    else:
        if trace.was_traced is True:
            return True
        else:
            if datetime.now(trace.task_active_ts.tzinfo) > trace.task_active_ts + timedelta(minutes=10):
                trace.task_active_ts = datetime.strptime('01.01.1990+0000', '%d.%m.%Y%z')
                trace.save()
                trace_with_sherlock.delay(name)
                return False
            elif datetime.now(trace.task_active_ts.tzinfo) <= trace.task_active_ts + timedelta(minutes=10):
                return True
            # elif trace.is_task_active is False:
            #     # start trace:
            #     # - add is_task_active, ts
            #     # execute sherlock script
            #     # - when done, add was_traced, return True
            #     ...
            else:
                raise NotImplementedError(errors['unknown_sherlock'])
