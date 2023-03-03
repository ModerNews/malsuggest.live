from celery import Celery
from .base_class import App
from .factory import create_app


def make_celery(app_name=__name__):
    backend = "redis://localhost:6379/0"
    broker = "redis://localhost:6379/1"
    celery = Celery(app_name, backend=backend, broker=broker, imports=('app.tasks', ))
    # TODO Pickle is unsafe - read more here: https://docs.celeryq.dev/en/latest/userguide/security.html#serializers
    # Implement client authorization
    celery.conf.task_serializer = 'pickle'
    celery.conf.result_serializer = 'pickle'
    celery.conf.accept_content = ['application/json', 'application/x-python-serialize']
    return celery


celery = make_celery()
