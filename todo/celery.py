from __future__ import absolute_import, unicode_literals
from celery.schedules import crontab

import os
from celery import Celery

# set the default Django settings module for the 'celery' program.
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'todo.settings')

app = Celery('todo')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

app.conf.update(
    BROKER_URL='redis://localhost:6379/',
    # broker_url = 'redis://user:password@redishost:6379/0',
    CELERY_DISABLE_RATE_LIMITS=True,
    CELERY_ACCEPT_CONTENT=['json', ],
    CELERY_TASK_SERIALIZER='json',
    CELERY_RESULT_SERIALIZER='json',
)

app.conf.beat_schedule = {
    'last_five_days': {
        'task': "todo_app.tasks.test",
        'schedule': 3600.0,
    }, }


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
