import celery
import malclient
from flask import current_app, render_template, request
from flask.blueprints import Blueprint

from .tasks import awaited_debug, calculate_personal_score

recommendations_blueprint = Blueprint(name='recommendations', import_name='recommendations_blueprint')


@recommendations_blueprint.get('/recommendations')
def recommendations_page():
    # TODO check if no additional processes started
    if not current_app.debug_value:
        client = malclient.Client(access_token=request.cookies["access_token"], refresh_token=request.cookies['refresh_token'])
        calculator_task: celery.Task = calculate_personal_score.delay(client, current_app.data_bank)
        return render_template('loading.html')
    else:
        return render_template('results.html')