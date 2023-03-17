import celery
import malclient
from flask import current_app, render_template, request, make_response
from flask.blueprints import Blueprint
from celery.result import AsyncResult

from .tasks import awaited_debug, calculate_personal_score

recommendations_blueprint = Blueprint(name='recommendations', import_name='recommendations_blueprint')


@recommendations_blueprint.get('/recommendations')
def recommendations_page():
    # TODO check if no additional processes started
    try:
        # Task finished
        task_id = request.cookies.get('task_id')
        task = AsyncResult(task_id)  # raises ValueError if cookie wasn't set
        print(task.status)
        return render_template('results.html')
    except ValueError:
        # task not even started
        client = malclient.Client(access_token=request.cookies["access_token"], refresh_token=request.cookies['refresh_token'])
        calculator_task: celery.Task = calculate_personal_score.delay(client, current_app.data_bank)
        current_app.database.create_task(calculator_task.id)
        current_app.debug_value = True
        response = make_response(render_template('loading.html'))
        response.set_cookie('task_id', calculator_task.id)
        return response