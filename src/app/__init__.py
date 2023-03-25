import os

from celery import Celery
from .base_class import App
from .factory import create_app


def make_celery(app_name=__name__):
    celery = Celery(app_name, backend=os.getenv("CELERY_RESULT_BACKEND"), broker=os.getenv("CELERY_BROKER_URL"), imports=('app.tasks', ))
    # TODO Pickle is unsafe - read more here: https://docs.celeryq.dev/en/latest/userguide/security.html#serializers
    # Implement celery client authorization
    celery.conf.task_serializer = 'pickle'
    celery.conf.result_serializer = 'pickle'
    celery.conf.accept_content = ['application/json', 'application/x-python-serialize']
    celery.conf.task_track_started = True
    return celery


celery = make_celery()
