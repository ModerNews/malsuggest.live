import logging
import base64
import zoneinfo
import os
import datetime

from flask import current_app, render_template, redirect, url_for, make_response, request, abort
from flask.blueprints import Blueprint

import malclient

__all__ = ['page_base_blueprint']

page_base_blueprint = Blueprint(name='page_base', import_name='page_base_blueprint',
                                template_folder='')


@page_base_blueprint.get('/')
def index():
    url, code_verifier = malclient.generate_authorization_url('48563b906310d3fdb4cefa1c1877bfc3')
    logging.info(code_verifier)
    response = make_response(render_template('index.html', redirect_url=url + '&redirect_uri=' + os.getenv('MAL_REDIRECT', 'http://127.0.0.1:5000/redirect')), 200)
    response.set_cookie('code_verifier', value=base64.b64encode(code_verifier.encode()).decode(),
                        expires=(datetime.datetime.now(tz=zoneinfo.ZoneInfo('Europe/London')) + datetime.timedelta(minutes=3)))
    return response


@page_base_blueprint.get('/redirect')
def redirect_receive():
    try:
        code_verifier = base64.b64decode(request.cookies.get('code_verifier').encode()).decode()
    except AttributeError:
        abort(410)
        return
    if not request.args.get('code'):
        abort(400)
        return
    token_response = malclient.fetch_token_schema_2(client_id=os.getenv('MAL_CLIENT_ID'),
                                                    client_secret=os.getenv('MAL_CLIENT_SECRET'),
                                                    code=request.args.get('code'),
                                                    code_verifier=code_verifier,
                                                    redirect_uri=os.getenv('MAL_REDIRECT', 'http://127.0.0.1:5000/redirect'))
    response = make_response(redirect(url_for('recommendations.recommendations_page')), 302)
    response.set_cookie('access_token', value=token_response.get('access_token'), samesite='Strict', expires=(datetime.datetime.now() + datetime.timedelta(seconds=int(token_response.get('expires_in')))))
    response.set_cookie('refresh_token', value=token_response.get('refresh_token'), samesite='Strict', expires=(datetime.datetime.now() + datetime.timedelta(seconds=int(token_response.get('expires_in')))))
    response.delete_cookie('code_verifier')
    return response