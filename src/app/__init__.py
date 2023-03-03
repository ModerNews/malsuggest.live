from celery import Celery
from .base_class import App
from .factory import create_app


def make_celery(app_name=__name__):
    backend = "redis://localhost:6379/0"
    broker = "redis://localhost:6379/1"
    return Celery(app_name, backend=backend, broker=broker, imports=('app.tasks', ))


celery = make_celery()
