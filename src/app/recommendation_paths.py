import celery
import malclient
from flask import current_app, render_template, request, make_response
from flask.blueprints import Blueprint

from . import celery as celery_instance
from .tasks import awaited_debug, calculate_personal_score

recommendations_blueprint = Blueprint(name='recommendations', import_name='recommendations_blueprint')


@recommendations_blueprint.get('/recommendations')
def recommendations_page():
    try:
        task_id = request.cookies['task_id']
        task = celery_instance.AsyncResult(task_id)
        if task.state in ("STARTED",):
            # Task is still running
            return render_template('loading.html')
        elif task.state in ("PENDING",):
            # Task status is unknown - Schedule new task
            print("Starting new task")
            raise ValueError('Task status is unknown')

        cache = current_app.database.get_cache_by_task_id(task_id)
        print(cache)
        if not cache:  # Checks if cache list, tuple, etc. is empty
            # TODO render response from cache
            return render_template('results.html', recommendations=cache)
            pass
        else:
            # Task state is known and finished, but no cache found in database
            raise ValueError('Cache for task not found in database')

    except (ValueError, KeyError):
        # task not even started
        client = malclient.Client(access_token=request.cookies["access_token"], refresh_token=request.cookies['refresh_token'])
        calculator_task: celery.Task = calculate_personal_score.delay(client, current_app.data_bank)
        current_app.database.create_task(calculator_task.id)
        current_app.debug_value = True
        response = make_response(render_template('loading.html'))
        response.set_cookie('task_id', calculator_task.id)
        return response