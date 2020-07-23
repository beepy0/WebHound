import requests, pytz, os.path, os, platform
from datetime import datetime, timedelta
from celery import shared_task
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse

from .models import Trace
from .config import errors, cfg_data


@shared_task
def trace_with_sherlock(name):
    try:
        trace = Trace.objects.get(pk=name)
        assert trace.task_active_ts >= cfg_data['default_task_ts']
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
                if trace.task_active_ts == cfg_data['default_task_ts']:  # no task started for this name yet
                    trace.task_active_ts = datetime.now(tz=pytz.utc)
                    trace.save()
                    cmd = cfg_data['sherlock_win_cmd'] if platform.system() == 'Windows' \
                        else cfg_data['sherlock_unix_cmd']
                    # execute sherlock script
                    os.system(cmd.format(trace.name, trace.name))
                    if os.path.isfile(cfg_data['sherlock_results_dir'].format(trace.name)) is True:
                        trace.was_traced = True
                        trace.task_active_ts = cfg_data['default_task_ts']
                        trace.save()
                        requests.put(cfg_data['root_url'].format(
                            reverse('WebHoundApp:hound_name', kwargs={'pk': trace.name})))
                    return True
                else:  # a task was started but has slowed/crashed
                    trace.task_active_ts = cfg_data['default_task_ts']
                    trace.save()
                    trace_with_sherlock.delay(name)
                    return False
            elif datetime.now(trace.task_active_ts.tzinfo) <= trace.task_active_ts + timedelta(minutes=10):
                return True
            else:
                raise NotImplementedError(errors['unknown_sherlock'])
