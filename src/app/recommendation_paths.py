from flask import current_app, render_template, request
from flask.blueprints import Blueprint

from .tasks import awaited_debug
recommendations_blueprint = Blueprint(name='recommendations', import_name='recommendations_blueprint')
print(awaited_debug.name)


@recommendations_blueprint.get('/recommendations')
def recommendations_page():
    if not current_app.debug_value:
        awaited_debug.delay()
        return render_template('loading.html')
    else:
        return render_template('results.html')