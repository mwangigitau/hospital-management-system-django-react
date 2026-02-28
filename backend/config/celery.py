import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')

app = Celery('hms')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'Request: {self.request!r}')


# Periodic tasks
app.conf.beat_schedule = {
    'cleanup-audit-logs-weekly': {
        'task': 'apps.accounts.tasks.cleanup_old_audit_logs',
        'schedule': crontab(hour=2, minute=0, day_of_week=0),
    },
}
