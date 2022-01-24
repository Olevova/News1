import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NewsSite.settings')

app = Celery('NewsSite')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.conf.beat_schedule = {
    'clear_board_every_minute': {
        'tasks': 'NewsSite.news.task.printer',
        'schedule': crontab(),
    },
}
app.autodiscover_tasks()