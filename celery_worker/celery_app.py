from __future__ import absolute_import, unicode_literals
from celery import Celery
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'geef.settings')

import django

django.setup()
from django.conf import settings
from celery_worker.tasks import my_hourly_task

app = Celery('geef')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)