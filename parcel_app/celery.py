from __future__ import absolute_import
import os
from celery import Celery
from django.conf import settings

settings.configure()

BROKER_URL = 'redis://localhost:6379/0'

os.environ.setdefault("DJANGO_SETTING_MODULE", "parcel_app.settings")
app = Celery("parcel_app")
app.config_from_object("django.conf:settings", namespace="CELERY")

app.conf.update(CELERY_RESULT_BACKEND=BROKER_URL)

app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))


@app.task
def add(x, y):
    return x + y

#
# task = add.delay(3, 5)
# print(task.status, task.result)
