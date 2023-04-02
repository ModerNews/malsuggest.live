from flask import current_app, render_template, make_response
from flask.blueprints import Blueprint

error_handler_blueprint = Blueprint(name='error_handlers', import_name='error_handlers_blueprint')


@error_handler_blueprint.app_errorhandler(410)
def code_verification_timeout(e):
    return render_template('errors/error.html', error_title='You were timed-out',
                           error_msg='What you were trying to do took too long, please try again')


@error_handler_blueprint.app_errorhandler(400)
def code_not_present(e):
    return render_template('errors/error.html', error_title='There was an error in your request',
                           error_msg='You did not provide code parameter')


@error_handler_blueprint.app_errorhandler(401)
def code_not_present(e):
    response = make_response(render_template('errors/error.html',
                                             error_title='You were logged out',
                                             error_msg='Your session token was invalidated and you were logged out, please try again'))
    response.delete_cookie('session_token')
    return


@error_handler_blueprint.app_errorhandler(404)
def page_not_available(e):
    return render_template('errors/error.html', error_title='Page not found',
                           error_msg='This probably means that the function you tried to use was not implemented yet')


@error_handler_blueprint.app_errorhandler(500)
def server_error(e):
    response = make_response(render_template('errors/error.html', error_title='Server error',
                           error_msg='It\'s on us this time! We\'ve cleared your session, please try again!'), 500)
    response.delete_cookie('session_token')
    response.delete_cookie('task_id')
    return response
