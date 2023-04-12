import os
from .settings import BASE_DIR
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")

app = Celery("backend")
app.config_from_object("django.conf:settings")

app.autodiscover_tasks()


app.conf.beat_schedule = {
    'country-task': {
      'task': 'country_update',
      'schedule': crontab(hour=7, minute=30, day_of_week=1)
    },
    'city-task': {
      'task': 'city_update',
      'schedule': crontab(hour=7, minute=30, day_of_week=1)
    }
}
