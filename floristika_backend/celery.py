import os

from celery import Celery
from django.conf import settings


# TODO: change in .production
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "floristika_backend.settings.production")

app = Celery("Floristika")

app.config_from_object("django.conf.settings", namespace="celery")

app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)