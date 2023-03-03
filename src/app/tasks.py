from flask import current_app
from . import celery, library

import os

from random import choice
import malclient

from friend_scrapper import get_user_friends

from flask_socketio import emit


@celery.task()
def awaited_debug(socket_id, namespace):
    with current_app.app_context():
        emit("response", {"message": "This is response message", "code": "200 OK"}, to=socket_id, namespace=namespace)
        print("Message sent")

