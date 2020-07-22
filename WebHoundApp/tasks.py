import pytz
from datetime import datetime, timedelta
from celery import shared_task
from django.core.exceptions import ObjectDoesNotExist

from .models import Trace
from .config import errors, data


@shared_task
def trace_with_sherlock(name):
    try:
        trace = Trace.objects.get(pk=name)
        assert trace.task_active_ts >= data['default_task_ts']
    except ObjectDoesNotExist:
        raise KeyError(errors['no_name_in_db'])
    except Exception:
        raise ValueError(errors['no_task_ts'])
    else:
        if trace.was_traced is True:
            return True
        else:
            # tasks that have ran more than 10 minutes without finishing need to be restarted
            if datetime.now(trace.task_active_ts.tzinfo) > trace.task_active_ts + timedelta(minutes=10):
                if trace.task_active_ts == data['default_task_ts']:  # no task started for this name yet
                    trace.task_active_ts = datetime.now(tz=pytz.utc)
                    trace.save()
                    ...
                    # execute sherlock script
                    # collect data
                    # store data
                    trace.was_traced = True
                    trace.task_active_ts = data['default_task_ts']
                    trace.save()
                    return True
                else:  # a task was started but has slowed/crashed
                    trace.task_active_ts = data['default_task_ts']
                    trace.save()
                    trace_with_sherlock.delay(name)
                    return False
            elif datetime.now(trace.task_active_ts.tzinfo) <= trace.task_active_ts + timedelta(minutes=10):
                return True
            else:
                raise NotImplementedError(errors['unknown_sherlock'])
