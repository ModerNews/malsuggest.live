import os

import celery
import malclient
from flask import current_app, render_template, request, make_response, Response, abort, g as flask_g, redirect
from flask.blueprints import Blueprint

from . import celery as celery_instance
from .tasks import awaited_debug, calculate_personal_score

recommendations_blueprint = Blueprint(name='recommendations', import_name='recommendations_blueprint')


def get_mal_data(cache: list[tuple]):
    """
    This is helper function used to generate presentable data (title and main picture) for the page from MAL API

    :returns: List of malclient.AnimeObject objects representing each cached result, and primary result
    :r_type: tuple[malclient.AnimeObject], malclient.AnimeObject
    """
    client = malclient.Client(client_id=os.getenv("MAL_CLIENT_ID"))
    cache, new_cache = list(cache[0]), []
    fields = malclient.Fields.node()
    print(cache)
    primary = client.get_anime_fields(cache[1], fields=fields)
    cache[2].remove(cache[1])
    for i in range(len(cache[2])):
        new_cache.append(client.get_anime_fields(cache[2][i], fields=fields))
    return tuple(new_cache), primary


def schedule_new_celery_task(tokens):
    """
    This is helper function, it creates malclient object, schedules calculate task and creates Flask response

    :returns: Loading page with customized cookies
    :r_type: Response
    """
    user_id, access_token, refresh_token = tokens
    client = malclient.Client(access_token=access_token, refresh_token=refresh_token)
    calculator_task: celery.Task = calculate_personal_score.delay(client, current_app.data_bank)
    current_app.database.create_task(calculator_task.id)
    current_app.debug_value = True
    response = make_response(render_template('loading.html'))
    response.set_cookie('task_id', calculator_task.id)
    return response


@recommendations_blueprint.before_request
def before_request():
    if request.path == '/recommendations' and 'session_token' in request.cookies:
        flask_g.tokens = current_app.database.get_mal_tokens_for_session(request.cookies['session_token'])
        if not flask_g.tokens:
            abort(401)


@recommendations_blueprint.get('/recommendations')
def recommendations_page():
    # TODO match tasks with users, create user database
    """
    Main function for /recommendations route, it follows simple scheme:
    First it tries to fetch celery task id from cookie
    If task_id is not present KeyErrror is raised, and new task is scheduled
    If task_id is present it's state is fetched from celery, then depending on the state:
    If task is started loading page is rendered
    If task is marked as pending it means it's state is unknown, due to that new task is scheduled
    Else cached data is fetched from DB
    If no data is found (it may be due to cache going stale, and being purged) error is raised, and new task is scheduled
    Else page with final results is rendered
    """
    try:
        print("Full stop")
        task_id = request.cookies['task_id']
        task = celery_instance.AsyncResult(task_id)
        if task.state in ("STARTED",):
            # Task is still running
            return render_template('loading.html')
        elif task.state in ("PENDING",):
            # Task status is unknown - Schedule new task
            raise ValueError('Task status is unknown')

        cache = current_app.database.get_cache_by_task_id(task_id)
        print(cache)
        if cache:  # False if cache (list, tuple, etc.) is empty
            cache, primary_result = get_mal_data(cache)
            return render_template('results.html', recommendations=cache, primary_result=primary_result)
        else:
            # Task state is known and finished, but no cache found in database
            raise ValueError('Cache for task not found in database')

    except (ValueError, KeyError):
        # task not even started
        return schedule_new_celery_task(flask_g.tokens)


@recommendations_blueprint.get('/anonymous')
def anonymous_search():
    # TODO implement anonymous search
    abort(404)