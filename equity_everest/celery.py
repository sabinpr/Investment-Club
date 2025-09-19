import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'equity_everest.settings')

app = Celery('equity_everest')

# Read config from Django settings, CELERY_ prefixed keys
app.config_from_object('django.conf:settings', namespace='CELERY')

# Auto-discover tasks in installed apps
app.autodiscover_tasks()

# Celery Beat Schedule
app.conf.beat_schedule = {
    'expire-proposals-daily': {
        'task': 'api.tasks.expire_old_proposals',
        # For testing purposes
        'schedule': crontab(minute='*/1'),  # every minute
        # 'schedule': crontab(hour=0, minute=0),  # Every day at midnight
    },
    'meeting-reminder-hourly': {
        'task': 'api.tasks.send_meeting_reminders',
        # For testing purposes
        'schedule': crontab(minute='*/1'),  # every minute
        # 'schedule': crontab(minute=0, hour='*/1'),  # Every hour
    },
    'test-celery-task': {
        'task': 'api.tasks.test_celery_task',
        # For testing purposes
        'schedule': crontab(minute='*/1'),  # every minute
    }
}

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
