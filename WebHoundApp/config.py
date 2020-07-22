from datetime import datetime

msgs = {
    'trace_not_done': 'Your trace is still not complete. Your hound should be back soon, either reload this page or type the same name in the homepage to check again.',
}

errors = {
    'no_trace_name': 'No trace name supplied',
    'no_name_in_db': 'The supplied trace name is not in the database',
    'no_task_ts': 'The task has no (default) timestamp',
    'unknown_sherlock': 'Unexpected branch for sherlock task logic',
}

data = {
    'default_task_ts': datetime.strptime('01.01.1990+0000', '%d.%m.%Y%z'),
}