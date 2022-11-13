from flask import current_app, make_response, render_template
from flask.blueprints import Blueprint

recommendations_blueprint = Blueprint(name='recommendations', import_name='recommendations_blueprint')


@recommendations_blueprint.get('/recommendations')
def recommendations_page():
    if not current_app.debug_value:
        current_app.debug_value = True
        return render_template('loading.html')
    else:
        return render_template('results.html')