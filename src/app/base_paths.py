import logging
import base64
import zoneinfo
import os
import datetime

import jwt

from flask import current_app, render_template, redirect, url_for, make_response, request, abort
from flask.blueprints import Blueprint

import malclient

__all__ = ['page_base_blueprint']

page_base_blueprint = Blueprint(name='page_base', import_name='page_base_blueprint',
                                template_folder='')

@page_base_blueprint.get('/')
def index():
    # TODO check if token is present in cookies after user preses "Anonymous Search" button
    url, code_verifier = malclient.generate_authorization_url('48563b906310d3fdb4cefa1c1877bfc3', redirect_uri=request.base_url + "redirect")
    logging.info(code_verifier)
    response = make_response(render_template('index.html', redirect_url=url), 200)
    response.set_cookie('code_verifier', value=base64.b64encode(code_verifier.encode()).decode(),
                        expires=(datetime.datetime.now(tz=zoneinfo.ZoneInfo('Europe/London')) + datetime.timedelta(minutes=3)))
    return response


def save_session_data_to_database(user_id, token, expires_in, token_response):
    current_app.database.create_session(user_id=user_id, token=token, expires_in=expires_in)
    current_app.database.create_mal_tokens(user_id=user_id,
                                           access_token=token_response.get('access_token'),
                                           refresh_token=token_response.get('refresh_token'))


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
                                                    redirect_uri=request.base_url)
    client = malclient.Client(access_token=token_response.get('access_token'),
                              refresh_token=token_response.get('refresh_token'))
    user = client.get_user_info()
    token = current_app.generate_session_token(user.id)
    response = make_response(redirect(url_for('recommendations.recommendations_page')), 302)
    response.set_cookie('session_token', value=token, samesite='Lax', expires=(datetime.datetime.now() + datetime.timedelta(seconds=int(token_response.get('expires_in')))))
    response.delete_cookie('code_verifier')
    save_session_data_to_database(user.id, token, token_response.get('expires_in'), token_response)
    return response