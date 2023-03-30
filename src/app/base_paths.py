import json
import logging
import base64
import random
import zoneinfo
import os
import datetime

import jwt
import secrets

from flask import current_app, render_template, redirect, url_for, make_response, request, abort
from flask.blueprints import Blueprint

import malclient

__all__ = ['page_base_blueprint']

page_base_blueprint = Blueprint(name='page_base', import_name='page_base_blueprint',
                                template_folder='')


def get_banner_params():
    try:
        with open('/home/anime_suggester/current_banner', 'r') as file:
            banner = file.read().replace(' ', '').replace('\n', '')
            assert file != ''
    except AssertionError:
        banner = random.choice(os.listdir('/home/anime_suggester/static/images/banners/'))
    with open('/home/anime_suggester/app/banners_options.json', 'r') as file:
        f = json.loads(file.read())
    try:
        banner_options = f[banner]
    except KeyError:
        banner_options = ''
    return banner, banner_options


@page_base_blueprint.get('/')
def index():
    banner, banner_options = get_banner_params()
    response = make_response(render_template('index.html', banner_file=f"../static/images/banners/{banner}", banner_options=banner_options), 200)
    token = secrets.token_urlsafe(100)
    code_verifier = token[:128]
    response.set_cookie('code_verifier', value=base64.b64encode(code_verifier.encode()).decode(),
                        expires=(datetime.datetime.now(tz=zoneinfo.ZoneInfo('Europe/London')) + datetime.timedelta(
                            minutes=3)))
    return response


def save_session_data_to_database(user_id, token, expires_in, token_response):
    current_app.database.delete_mal_tokens_with_user_id(user_id)  # First deleting all tokens for given user that went stale
    current_app.database.create_session(user_id=user_id, token=token, expires_in=expires_in)
    current_app.database.create_mal_tokens(user_id=user_id,
                                           access_token=token_response.get('access_token'),
                                           refresh_token=token_response.get('refresh_token'))


def validate_mal_tokens(user_id, access_token, refresh_token) -> bool:
    """
    Simple helper function, raises false if request against the API fails
    This mainly happens if token pair is revoked
    """
    try:
        client = malclient.Client(access_token=access_token, refresh_token=refresh_token)
        return True
    except:
        return False


@page_base_blueprint.get('/verify')
def redirect_verify():
    method = request.args.get('method')
    if method == 'login':
        try:
            tokens = current_app.database.get_mal_tokens_for_session(request.cookies['session_token'])
            valid = validate_mal_tokens(*tokens)
            if not tokens:
                # Delete revoked token pair from database
                current_app.database.delete_mal_tokens_with_user_id(tokens[0])
                raise ValueError("Token pair has been revoked by MAL")
            else:
                response = make_response(redirect('/recommendations'))
                response.delete_cookie('code_verifier')
                return response
        except (KeyError, ValueError):
            logging.info("There is no valid token data available")
    if method == 'anonymous':
        # TODO currently anonymous points to 404 page, implement anonymous search
        pass
    try:
        code_verifier = base64.b64decode(request.cookies.get('code_verifier').encode()).decode()
        url, code_verifier = malclient.generate_authorization_url(os.getenv("MAL_CLIENT_ID"),
                                                                  redirect_uri=request.root_url + "redirect",
                                                                  code_verifier=code_verifier)
        return redirect(url)
    except KeyError:
        abort(410)


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
    response.set_cookie('session_token', value=token, samesite='Lax', expires=(
                datetime.datetime.now() + datetime.timedelta(seconds=int(token_response.get('expires_in')))))
    response.delete_cookie('code_verifier')
    save_session_data_to_database(user.id, token, token_response.get('expires_in'), token_response)
    return response
