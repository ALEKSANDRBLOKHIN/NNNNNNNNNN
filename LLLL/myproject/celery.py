import os
from celery import Celery
from celery.schedules import crontab
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')

app = Celery('myproject')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


app.conf.beat_schedule = {
    'send_weekly_news_every_week': {
        'task': 'news_list.tasks.send_weekly_news',
        'schedule': crontab(hour=0, minute=0, day_of_week='monday'),
    },
}


app.conf.beat_schedule = {
    'send_weekly_newsletter': {
        'task': 'news_list.tasks.send_weekly_newsletter',
        'schedule': crontab(hour=8, minute=0, day_of_week='monday'),
    },
}

