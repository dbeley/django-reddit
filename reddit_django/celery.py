from __future__ import absolute_import, unicode_literals

import os

from celery import Celery

# set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "reddit_django.settings")

# app = Celery("reddit_django", backend="redis://localhost", broker="pyamqp://")
app = Celery("reddit_django")

if os.environ.get("REDIS_URL"):
    app.conf.update(
        BROKER_URL=os.environ["REDIS_URL"],
        CELERY_RESULT_BACKEND=os.environ["REDIS_URL"],
    )
    # print("Deployment configuration.")
    # CELERY_BROKER_URL = os.environ["REDIS_URL"]
    # CELERY_RESULT_BACKEND = os.environ["REDIS_URL"]
    # CACHES = {
    #     "default": {
    #         "BACKEND": "redis_cache.RedisCache",
    #         "LOCATION": os.environ.get("REDIS_URL"),
    #     }
    # }

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object("django.conf:settings", namespace="CELERY")

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print("Request: {0!r}".format(self.request))
