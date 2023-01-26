import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

app = Celery('backend')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


app.conf.beat_schedule = {
    'raise-debt-every-3-hours': {
        'task': 'companies.tasks.raise_debt_random',
        'schedule': crontab(minute=0, hour='*/3')
    },
    'reduce-debt-at-6.30am': {
        'task': 'companies.tasks.reduce_debt_random',
        'schedule': crontab(minute='30', hour='6')
    },
}
